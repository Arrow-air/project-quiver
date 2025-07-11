<!--Chinese language comparison included 包含汉语对照-->
# Status 

Draft

# Project Description

由于Quiver项目长期以来使用3D打印方法制作原型和部分产品的结构件，但缺乏对其强度的具体研究，且传统的FEA（有限元分析）工作流程仅适用于匀质部件，无法为3D打印件提供可靠分析结果。为了解决这个问题，现决定收集并整理一些学术知识，以增进我们对3D打印结构的了解，并在成本可控的前提下改良我们的3D打印结构设计流程。

# Methodology 

结合过往的3D打印操作经验，在网络上搜索和整理相关的研究成果和论文

# Results and Deliverables 

## Overview

通常3D打印（增材制造）部件无法通过使用均质参数的FEA得出正确结果，有以下主要原因：

1. 打印轨迹产生的不均匀强度分布和微观间隙，
2. 各类不同设计下的层厚、infill密度和壁厚度。
3. 层内和层间的分子连接方式不同，导致XY/XZ强度区别巨大。

这些特性导致3D打印件需要以各向异性的方法来求解，并且需要针对宏观或微观需求来定制不同的工作流程。

围绕Fusion和Inventor，

## Compare To Injection Molding

3D打印件的强度、均匀度和材料选项，在相同重量下远无法匹敌注塑件。但从生产周期和性价比上看，3D打印工艺则有绝对优势。以下是两者的一些对比：

|-|3D Printing|Injected Molding|
|-|-|-|
|Material characteristics|Anisotropy|Isotropic *|
|Material Options|Single filament|Multi-ingredient pellet mixable|
|Material Requirement|Higher thermal / humidity stability|Less additive required|
|Material Source|Common plastics (ABS, PETG, PA...)|More specialty plastics (PC, PEEK, PTE...)|
|-|-|-|
|Build Pressure|1 ~ 35 Mpa (Gear extrude)|35 ~ 100 Mpa (Hydraulic screw press)|
|Typical XY Tensile Modulus (GPa)|1.6 ~ 2.2 (x0.8)|2.0 ~ 2.4 (x1.0)|
|Typical XZ Tensile Modulus (GPa)|0.8 ~ 1.3 (x0.4)|-|
|Dimensional Accuracy|0.01 ~ 0.3 mm|＜ 0.01 mm|
|-|-|-|
|Design-To-Product Time|In hours|More than weeks|
|Starting Cost|$ 0.1|$ 1000|

 \* Controllable depends on different injection point designs. May use with simulator software such as Autodesk Moldflow.

## Practical Solution

可以通过以下方法进一步提高打印强度

1. 提高打印温度
2. 足量的退火后处理
3. 尽量减小打印层高
4. Use Brick layer slicing. For most non-fiber filaments, XZ strength can be improved by 10% during tensile testing, but this has not yet been verified by FEA.

## Uncharted Knowledge

|Items|Description|
|-|-|

# Remarks 
