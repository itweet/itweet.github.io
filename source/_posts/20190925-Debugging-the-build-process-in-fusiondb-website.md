---
title: Debugging the build process in fusiondb website
date: 2019-09-25 15:46:20
description: 利用大前端技术构建 FusionDB 纯静态的官方网站，遇到的一些小坑，纯粹记录一下备忘。
tags: [Debug, 2019]
category: Web Design
---

曾经在构建 `Core Data & Core AI` 统一分析平台 [`JDP`](http://www.fusionlab.cn/zh-cn/) 时，就面临一个编写文档的窘境，系统功能构建太快，早期由于没有规划和约束导致大量的功能并未编写文档以及遵守良好的编程风格，导致最后查无所依，软件维护成本高昂。与一些公开的公益性质的开源持续集成服务也没用很好的结合，造成大量的工作依赖手工完成，甚至自己组装服务器在家进行各种压测以及持续集成的工作。

如上一些原因，我就在思考如何才能在软件开发初期较早的版本就开始规避类似的问题呢？

首先，我们完全遵守国际化的标注进行软件的开发工作，利用 Git 和 Github 提供的相关软件开发流程管理工具，标准化整个 PR 的提交流程，参见: [Build an official website](https://github.com/FusionDB/fusiondb.github.io/pull/2)。

* 可信赖、可持续发展的软件系统，文档和代码一定同等重要
* Issues 或 Jira 管理全部的软件 Feature 开发，做到追溯，查有所依
* Pull requet 经过严格的 Review/QA
* 每个 Pull requet 做到功能的独立性，不掺杂任何无关的代码提交，清晰的区分 bugfix、feature、hotfix
* 模块众多，逻辑划分清晰，做到每个 PR 带有相应模块标识
* 每个新功能的开发或者大的变更都应编写相关设计与实现文档进行集体 review
* 每个新功能或者已有功能的变更，都需要详细记录在相关的设计文档中
* 每增加一个功能，需要相应的编写用户使用文档，进行详细的阐述新功能的使用方法，带有示例代码

有点跑偏了，我们今天主要讨论，构建一个可信赖的 Open Source 项目的官方网站。需要涉及哪些内容，有哪些可以信赖的开源服务，帮助我们快速达成目标。

* 首先，确定官方网站一定是静态的 HTML 页面，需要方便随时修改并发布
* 文档项目主流都是基于 Markdown 语法，故需要能对 markdown 渲染成静态 HTML
* 需要能对接持续集成工具自动化的 Build 并发布到线上
    - 需要支持全文检索文档功能，方便用户使用，调研一圈选定：Algolia index 服务
    - Algolia index 使用，按照官方文档的方式嵌入到每次 Build 的流程自动 Push 到此服务
* 集成 google analytics & tagmanager 服务方便分析网站的整个访问指标
    - 按照 google analytics & tagmanager 服务集成文档说明
    - 注册账号申请相应的使用 ID，在 fusiondb website 文档项目配置文件配置
* SEO 优化，比如：官方网站关键词的选择，搜索引擎友好，带来流量提升

接下来，关于内容的构建，极为关键。文档的质量和内容直接决定未来用户基数。为了解决一开始我提出的一些问题，我单独构建出一个 Design 栏目，追踪整个项目的设计理念以及每个 Feature 的详细设计，包括调研、实现、设计的权衡。Apache 一些比较成熟的顶级项目基本都有详设的文档，比如: 

* [SPIP: Spark API for Table Metadata](https://docs.google.com/document/d/1zLFiA1VuaWeVxeTDXNg8bL6GP3BVoOZBkewFtEnjEoo/edit#)

* [[DESIGN] Ground Source Sink Concepts in Flink](https://docs.google.com/document/d/1yrKXEIRATfxHJJ0K3t6wUgXAtZq8D-XgvEnvl2uUcr0/edit#heading=h.oqvjdqvo5bkh)

在 Google Docs 上直接多人协作和 Review，一起修订，在社区发起广泛会议讨论，投票提案阶段，提案通过，进入研发排期。

我终于要进入正题啦。。。

感慨大前端好复杂，N 种构建工具、前后端分离框架、微服务真是够复杂的，曾经就简单写过 JQuery、JavaScript、HTML、CSS。现在的大前端真是复杂多了，各种新概念词。

为调试一个遇到的 Bug，3 个多小时没搞定，专门请教了专业人士，最终才解决问题。

Bug 有些诡异：`yarn start` 渲染的静态页面没问题，`yarn build && yarn serve` 出来的界面有问题。初步定位 `build` 和 `start` 执行的命令不一样，多次调试无果，最后发现是较低级错误，在代码中判断 `development` 和 `production` 执行的代码不一致，导致某个页面渲染获取到了空值，页面渲染异常。

我们来学习下，如何进行大前端 Debug 吧，适合初学小白。。。

项目主要是 Node.js 为运行环境，可以利用 Node.js 提供的 debug 工具进行调试。

我们主要介绍使用以下几种方法进行代码的调试：

* VS Code debugger (Manual-Config)
* Chrome DevTools for Node

## VS Code debugger (Manual-Config)

在编辑器中进行调试将会非常方便，可以跳过在 Chrome DevTools 相关的繁琐配置。可以将断点设置在你代码的具体某一行，并且能直观的看到相应的上下文信息。

我在这里不会过多解释 VS-Code 如何进行调试，学习 [VS Code debug 技巧](https://code.visualstudio.com/docs/editor/debugging)。我们仅共享一下 Gatsby.js 相关的 vs-code debug 配置。

关于 `.vscode/launch.json`

```
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Gatsby develop",
      "type": "node",
      "request": "launch",
      "protocol": "inspector",
      "program": "${workspaceRoot}/node_modules/gatsby/dist/bin/gatsby",
      "args": ["develop"],
      "stopOnEntry": false,
      "runtimeArgs": ["--nolazy"],
      "sourceMaps": false
    },
    {
      "name": "Gatsby build",
      "type": "node",
      "request": "launch",
      "protocol": "inspector",
      "program": "${workspaceRoot}/node_modules/gatsby/dist/bin/gatsby",
      "args": ["build"],
      "stopOnEntry": false,
      "runtimeArgs": ["--nolazy"],
      "sourceMaps": false
    }
  ]
}
```

在 gatsby-node.js 中设置断点并使用 VS Code 中的 Start debugging 命令后，您可以看到最终结果：

![](https://www.itweet.cn/screenshots/vscode-debug.png)

> 注意: 如果断点没有在 `const value = createFilePath({ node, getNode })` 生效，你可以运行 `gatsby clean` 命令删除 `.cache` 和 `public` 目录，然后重试。

## Chrome DevTools for Node

### Running Gatsby with the inspect flag

在项目目录中运行如下命令，而不是 `npm run develop`。

```
node --inspect-brk --no-lazy node_modules/gatsby/dist/bin/gatsby develop
```

* --inspect-brk will enable Node's inspector agent which will allow you to connect a debugger. It will also pause execution until the debugger is connected and then wait for you to resume it.
* --no-lazy - 这将迫使 Node 的 V8 引擎禁用延迟编译，便于设置断点。

### Connecting DevTools

在 Chrome 浏览器中键入 `chrome://inspect`，通过单击 `inspect` 连接到远程目标。

![](https://www.itweet.cn/screenshots/chrome-devtools-inspect.png)

你应该能看到 Chrome DevTools 启动，代码执行在 `gatsby.js` 入口文件的开始处暂停。

![](https://www.itweet.cn/screenshots/chrome-devtools-init.png)

### 设置 `Sources Code`

在浏览器中可以选择添加一个本地的目录到 `Sources`。

### Using DevTools

添加本地项目到 `Sources` 中，就可以在浏览器的代码页面单机代码行号设置断点，进行愉快的调试了。

## 完

总体来看在 IDE 中进行代码调试是非常方便的，而使用 Chrome DevTools 并不是那么的方便。

## Reference

* [debugging-getting-started](https://nodejs.org/en/docs/guides/debugging-getting-started/)
* [Debugging with Node.js - Paul Irish talk at Node Summit 2017](https://www.youtube.com/watch?v=Xb_0awoShR8)
* [debugging-the-build-process](https://github.com/gatsbyjs/gatsby/blob/master/docs/docs/debugging-the-build-process.md)

![Whoami公众号](https://github.com/itweet/labs/raw/master/common/img/weixin_public.gif)

原创文章，转载请注明： 转载自[Itweet](http://www.itweet.cn)的博客
`本博客的文章集合:` http://www.itweet.cn/archives/