# 跨工作区恢复与继续制作

当前目录已持久保存此前仅在旧会话 scratch 中的制作脚本。路径以本目录所在项目为基准，不依赖旧 `/workspace/cc-practice` 或 `/workspace/scratch`。

## 先恢复文件

运行仓库 `传送/恢复校园工作区.py --target 当前项目/校园完整工作区`。它用标准库下载已核验的 V3 包与制作资料包，安装到全新目录，保存逐文件SHA256清单。目标已存在且内容一致时只验证，不重写；内容有变、目标非空或含符号链接时拒绝覆盖。原有不完整的 cc-practice 无需删除或搬走。

恢复后打开 `校园建筑修复版/打开校园.html` 即可离线运行；读取或直接编辑运行版不需要先装构建依赖。

## 继续生成建筑和道路

安装构建依赖与安装文件是两件事。构建依赖锁定为Shapely 2.2.0、Pillow 12.3.0；浏览器核验另需 Node.js、Playwright和Chromium。

```sh
python 制作工具/安装依赖.py --browser
.venv/bin/python 制作工具/继续制作.py --verify-reproduction
```

Windows 的虚拟环境 Python 为 `.venv/Scripts/python.exe`。生成入口默认输出到 `工作输出/校园建筑修复版`，不会覆盖已发布基线。该输出已存在时指定新的 `--output`。`--verify-reproduction` 用于确认未修改生成源时关键文件与已发布 V3 一致；有意改了生成源后，不使用这个要求逐字相同的选项。

正式有效源是 `building-repair/prepare_scene.py`、`build_runtime.py`、`prototype_facades.js`、`camera_controls.js`、`camera_view.js`。从任意 cwd 调用继续制作入口都使用工具所在项目为根目录。新输出不会继承 V3 的旧截图与独立验收报告。

## 核验新输出

```sh
CAMPUS_OUTPUT_DIR="$PWD/工作输出/校园建筑修复版" node 制作工具/building-repair/validate.cjs
CAMPUS_OUTPUT_DIR="$PWD/工作输出/校园建筑修复版" node 制作工具/building-repair/catalog.cjs
CAMPUS_OUTPUT_DIR="$PWD/工作输出/校园建筑修复版" node 制作工具/building-repair/capture_final.cjs
```

设置 `CAMPUS_CHROMIUM` 可指定已安装的 Chromium。`document.py` 可生成对照文档和俯视图，需 Pillow及可用中文字体。`.venv`和`node_modules`不随恢复包复制，使用安装入口在新工作区建立。

依赖安装使用本项目 `.cache/pip`、`.cache/npm` 和 `.cache/ms-playwright`，无需修改用户主目录或申请系统目录写权限。系统 Chromium 优先，显式设置的 `PLAYWRIGHT_BROWSERS_PATH` 予以保留。

## 原动作与原始工程

`original-motion/export-project` 保留原绘制脚本和可重导出的 Godot 工程，不包含导入缓存。已有图集、帧表和原件均已保存，改楼不需要重新导出人物。导出输出默认在 Godot 的 user://motion-export；也可用环境变量 CAMPUS_MOTION_OUTPUT 指向新目录，不覆盖原图集。

完整原Godot仓库固定版本见项目根目录 `原工程固定版本.json`。浏览器版、恢复包和原Godot全工程不同；需要原游戏的室内或剧情时，从该仓库固定提交单独恢复并拉取Git LFS资源：

```sh
git clone https://github.com/i-m-not-sufer/sufe-campus-adventure.git sufe-campus-adventure
git -C sufe-campus-adventure checkout --detach 5cc649fdf5618df8177251ef59eaed7d6af1e495
git -C sufe-campus-adventure lfs pull
```

这一步不是恢复浏览器V3的前置条件，不会默认下载538MiB的队友原始Windows包。

## 历史存档

`历史存档/` 是旧脚本的原样备份，含旧路径和旧版本行为。尤其历史 `package.py`、`package_architecture.py` 会清理或覆盖发布文件，**不能作为新环境默认执行入口**。历史脚本、必要原件、原型照片和校方参考图已保存在仓库／恢复资料包中；系统工具二进制、缓存及未使用的抓取照片不作为制作依赖。

`参考资料/sufe-official-map.jpg` 为2023校方参考图，与用户初图有局部差异，用户初图和红蓝批注优先。恢复资料包中的 `校园建筑版`、`校园动作继承版` 仅保存当前生成链要读取的基线文件，不标为完整旧试玩版本；最新完整可玩版本是 `校园建筑修复版`。
