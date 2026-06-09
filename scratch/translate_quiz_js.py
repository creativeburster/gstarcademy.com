import os

QUIZ_JS_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'quiz.js')

with open(QUIZ_JS_PATH, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. 替换 QUIZ_DATABASE 中的中文标题和描述
database_translations = {
    # BIM
    'title: "Lesson 1: 热身测验 (Warmup)"': 'title: "Lesson 1: Warmup"',
    'desc: "BIM 核心范式、LOD 精度等级、协作流程与标准"': 'desc: "BIM Paradigms, LOD Standards, & CDE Workflow"',
    'title: "Lesson 2: 核心概念 (Core Concepts)"': 'title: "Lesson 2: Core Concepts"',
    'desc: "Autodesk Revit 族系统、多学科共享坐标系与三维扫描对齐"': 'desc: "Revit Family System, Shared Coordinates, & Scan-to-BIM"',
    'title: "Lesson 3: 实操避坑 (Common Pitfalls)"': 'title: "Lesson 3: Common Pitfalls"',
    'desc: "Navisworks 碰撞检测、IFC 格式导出设置与 4D/5D 工程模拟"': 'desc: "Navisworks Clashes, IFC Settings, & 4D/5D Simulation"',
    
    # MCAD
    'desc: "MCAD 几何约束意图、SOLIDWORKS 配置管理与 PDM 版本控制"': 'desc: "Geometric Constraints, SOLIDWORKS Configurations, & PDM"',
    'desc: "B-Rep 拓扑边界表达、三维装配自由度约束与 FEA 有限元分析网格收敛"': 'desc: "B-Rep Topology, Assembly Degrees of Freedom, & FEA Mesh"',
    'desc: "模型定义 MBD 标准化、模具拔模检测与钣金展平 K-Factor 计算"': 'desc: "MBD Standards, Mold Draft Check, & Sheet Metal K-Factor"',
    
    # Civil
    'desc: "TIN 地形表面模型、Civil 3D 软件架构与 COGO 点 Description Key 自动处理"': 'desc: "TIN Surfaces, Civil 3D Architecture, & Description Keys"',
    'desc: "道路平纵曲线关联设计、重力流管网规则与放坡组 (Grading Group) 动态平衡"': 'desc: "Road Profiles, Gravity Pipe Rules, & Grading Groups"',
    'desc: "道路装配部件目标映射、GPS 数字化施工 LandXML 导出与土方量核算"': 'desc: "Road Subassemblies, LandXML Field Export, & Earthworks"',
    
    # 2D Draft
    'desc: "2D 图层状态管理、PGP 快捷键命令别名与 AutoLISP 脚本自动定制"': 'desc: "Layer States, Command PGP Aliases, & AutoLISP Scripts"',
    'desc: "外部参照 Xref 协同管理、图纸视口比例打印与动态块参数设计"': 'desc: "Xref Management, Paper Space Viewports, & Dynamic Blocks"',
    'desc: "DWG 图纸版本图层差异比对、多视口下注释性比例 (Annotative) 缩放与冲突消解"': 'desc: "DWG Compare, Annotative Scaling, & Scale Conflicts"',
}

for src, dest in database_translations.items():
    content = content.replace(src, dest)

# 2. 替换状态和备份提示中的中文
ui_translations = {
    # Streak & backup
    '🔥 ${streak} 天': '🔥 ${streak} Days',
    '"📋 进度恢复码已成功复制到剪贴板！请妥善保存。"': '"📋 Progress recovery code copied to clipboard!"',
    '"📋 进度恢复码已选择并复制！"': '"📋 Progress recovery code selected and copied!"',
    '"❌ 请先输入有效的进度恢复码。"': '"❌ Please enter a valid recovery code."',
    '"❌ 无效的恢复码，版本不匹配或格式有误。"': '"❌ Invalid recovery code format or version mismatch."',
    '"🎉 进度恢复成功！页面即将刷新加载最新数据..."': '"🎉 Progress restored successfully! Reloading..."',
    '"❌ 还原失败，恢复码无效或已损坏，请确保复制完整。"': '"❌ Restore failed. Recovery code is invalid or corrupted."',
    
    # Lesson portal tags
    '已通关 ✅': 'Passed ✅',
    '重新挑战': 'Review',
    '可开始 🟢': 'Active 🟢',
    '开始挑战': 'Start',
    '已锁闭 🔒': 'Locked 🔒',
    
    # Subtitle
    '"依次完成以下小课以解锁该职业路径的技能树节点并获取经验值！"': '"Complete each bite-sized lesson sequentially to master this career track and unlock all roadmap nodes!"',
    
    # Failure Screen
    '"定级未通过"': '"Placement Test Failed"',
    '"您在定级测试中生命值耗尽，或者正确率未达到 80%。别灰心！从基础单项测验开始，能帮您快速查漏补缺。"': '"You ran out of lives or scored below 80%. Don\'t give up! Try starting with the core lessons to build up your skills."',
    '"🔁 重新定级测试"': '"🔁 Retry Placement Test"',
    '"📚 浏览 Wiki"': '"📚 Browse Wiki"',
    '"挑战失败"': '"Lesson Failed"',
    '"您在本次挑战中生命值已耗尽。没关系，多在 Wiki 中学习原子概念，下次一定能成功！"': '"You ran out of lives in this challenge. Reviewing the atomic concepts in our Wiki will help you conquer it next time!"',
    '"🔁 重新开始本课"': '"🔁 Retry Lesson"',
    '"📋 返回关卡中心"': '"📋 Back to Portal"',
    
    # Success Screen
    '"定级通关成功！"': '"Placement Test Passed!"',
    '"太棒了！您成功通过了综合入学定级测验，证明了自己深厚的 CAD 实战经验。"': '"Great job! You\'ve successfully passed the comprehensive placement test, demonstrating strong CAD competency."',
    '"🎯 <strong>路线图点亮：</strong> 恭喜！全站所有 4 大职业路径共 20 个技能节点已被全部同步点亮！"': '"🎯 <strong>Roadmap Synced:</strong> Congratulations! All 20 skill nodes across all 4 pathways have been fully lit up!"',
    '"🗺️ 查看技能地图"': '"🗺️ View Learning Map"',
    '"🔄 挑战其他职业路径"': '"🔄 Try Other Pathways"',
    '"单元通关成功！"': '"Unit Completed!"',
    '`恭喜！您已成功通关 ${track.trackTitle} 的全部课程！`': '`Congratulations! You have successfully completed all lessons for the ${track.trackTitle} track.`',
    '"🎯 <strong>技能树已点亮：</strong> 恭喜！本单元在技能地图上的 5 个核心节点已被全部点亮，并同步更新至您的 Wiki 概念库中！"': '"🎯 <strong>Roadmap Synced:</strong> Congratulations! All 5 core nodes on the skill map have been lit up and added to your concept library."',
    '"小课挑战成功！"': '"Lesson Completed!"',
    '`恭喜通关 ${lesson.title}！您已经掌握了本小课的核心概念。`': '`Congratulations on passing ${lesson.title}! You have mastered the core concepts of this lesson.`',
    '"🎯 <strong>下一课已解锁：</strong> 继续挑战下一课，完整通关本单元以点亮技能树！"': '"🎯 <strong>Next Lesson Unlocked:</strong> Continue to the next challenge, or finish the unit to light up the skill tree!"',
    '"➡️ 继续下一课"': '"➡️ Continue"',
    '"📋 返回关卡中心"': '"📋 Back to Unit Portal"',
}

for src, dest in ui_translations.items():
    content = content.replace(src, dest)

with open(QUIZ_JS_PATH, 'w', encoding='utf-8') as f:
    f.write(content)

print("Translation completed successfully for quiz.js!")
