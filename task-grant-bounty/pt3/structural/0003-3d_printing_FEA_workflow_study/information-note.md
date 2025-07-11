<!--Chinese language comparison included 包含汉语对照-->
# Status 

Draft

# Project Description

由于Quiver项目长期以来使用3D打印方法制作原型和部分产品的结构件，但缺乏对其强度的具体研究，且最初级的FEA（有限元分析）工作流程仅适用于均质部件，无法为3D打印件提供可靠结果。为了解决这个问题，现决定收集并整理一些学术知识，以增进我们对3D打印结构的了解，并在成本可控的前提下改良我们的3D打印结构设计流程。

同时，将收集一些注塑相关的参数，与3D打印件进行比较。

# Methodology 

将结合过往的3D打印操作经验，并在网络上搜索和整理相关的研究成果和论文，同时将收集到的资料交由AI助手ChatGPT-O3进行交叉比对。必要时将使用Inventor或Fusion进行实操和求解（可能消耗Token）。

# Results and Deliverables 

## Overview

通常3D打印（增材制造）部件无法通过使用均质参数的FEA得出正确结果，有以下主要原因：

1. 打印轨迹产生的不均匀强度分布和微观间隙，
2. 各类不同设计下的层厚、infill密度和壁厚度。
3. 层内和层间的分子连接方式不同，导致XY/XZ强度区别巨大。

这些特性导致3D打印件需要引入正交各向异性的参数来求解，并且需要针对宏观或微观需求来定制不同的工作流程。

## Software Selection

|Software|Functions|Availability|
|-|-|-|
|Fusion|Simulation for homogeneous or isotropic material|No (Can't match the current needs)|
|Inventor (with Nastran)|Simulations for orthotropic
|Siemens NX|Anisotropic |No (Expensive)|
|Netfabb|Wall/infill preparation and heat/stress simulation for 3D printing process|No (Expensive)|
|Digimat|Representative elementary volume (RVE) microscopic simulation|No (Too micro for current needs)|

目前，各类支持各向异性和微观结构模拟的CAD软件都非常昂贵，所以此information note将主要围绕Fusion或Inventor支持的功能进行解释。

## FEA Preparation

TBD 正确的参数？

TBD 正确的切片方式？

在使用FEA求解前，需要以手动的方式将模型抽壳，并将其中填入预取的infill模板

## FEA workflow



## Actual Manufacturing

可以通过以下方法进一步提高打印强度：

|Items|Theory|
|-|-|
|Increase the printing temperature|Increase interlayer fusion connection and reduce cooling gradient|
|Sufficient annealing treatment|Make molecular chains better connected and reduce internal stress
|Minimize the print layer height|
|Use Brick layer slicing|For most non-fiber filaments, XZ strength can be improved by 5 ~ 10 % during tensile testing, but this has not yet been verified by FEA|

## Compare To Injection Molding

3D打印件的强度、均匀度和材料选项，在相同重量下远无法匹敌注塑件。但从生产周期和性价比上看，3D打印工艺则有绝对优势。以下是两者的一些对比：

|-|3D Printing|Injected Molding|
|-|-|-|
|Material characteristics|Anisotropy|Isotropic *|
|Material Options|Single filament|Multi-ingredient pellet mixable|
|Material Property|Higher thermal / humidity stability|Higher liquidity, Less additive required|
|Material Source|Common plastics (ABS, PETG, PA...)|More specialty plastics (PA-GF, PC, PAEK, PTE...)|
|-|-|-|
|Build Pressure|1 ~ 35 Mpa (Gear extrude)|2 ~ 200 Mpa (Hydraulic screw press)|
|Typical XY Tensile Modulus (GPa)|1.6 ~ 2.2 (x0.8)|2.0 ~ 2.4 (x1.0)|
|Typical XZ Tensile Modulus (GPa)|0.8 ~ 1.3 (x0.4)|-|
|Dimensional Accuracy|0.01 ~ 0.3 mm|＜ 0.01 mm|
|-|-|-|
|Design-To-Product Time|In hours|More than weeks|
|Starting Cost|$ 0.1|$ 1000|

 \* Controllable depends on different injection point designs. May use with simulator software such as Autodesk Moldflow.

## Uncharted Knowledge

# Remarks 
