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

通常3D打印（增材制造）部件无法通过使用均质参数的FEA得出正确结果，在宏观方面有以下主要原因：

1. 各类不同的层厚、壁厚和infill密度设计，会直接影响力在部件内的传递。
2. 层内的耗材分子连接连续性好，就像玻璃受热相变后又冷凝为单体。而层间则为较弱的二次熔融扩散连接，就像两块一经解冻又再次冷冻的肉，外壁相互之间粘合。这个特征导致部件的XY与XZ之间强度差别巨大。

这些特性导致3D打印件需要引入正交各向异性的方法来求解，并且各种不同的密度和填充参数均需要定制不同的工作流程。总而言之，相对于均质部件，3D打印部件的FEA流程实际上变化多样。

微观方面则有下列影响，虽然以我们现有技术手段无法对它们进行系统性的分析，但依然值得列出并关注：

1. 切片软件产生的转角、过挤出、欠挤出，以及速度和压力曲线的变化，导致的不均匀线宽、微观间隙、碳化差异等。
2. 长时间打印，不同层之间因为温度梯度而产生的内应力（同时也是部件翘曲的原因）。
3. 在不同环境下保存或不同厂家生产的耗材质量，其中的杂质会对整体强度造成影响，例如水汽等。


## Software Selection

|Software|Functions|Availability|
|-|-|-|
|Fusion|Simulation for homogeneous or isotropic materials|No (Can't match the current needs)|
|Inventor (with Nastran)|Simulations for orthotropic materials|Yes (Cheap and well-functioning|
|Siemens NX|Simulations for orthotropic materials|No (Expensive)|
|Netfabb|Wall/infill preparation and heat/stress simulation for 3D printing process|No (Expensive)|
|Digimat|Representative elementary volume (RVE) microscopic simulation|No (Too micro for current needs)|

目前，大部分支持正交各向异性和微观结构模拟的CAD软件都非常昂贵，所以此information note将主要围绕Fusion或Inventor支持的功能进行解释。

## Material Data Preparation

TBD 正确的参数？
1、从厂家的参数表获得 
2、使用ASTM D638兼容的Tensile testing machine
3、以上哪种是最佳方法？

### From Manufacturer's parameter card

### From Tensile Testing Machine Result



## FEA workflow

TBD 正确的切片方式？

在使用FEA求解前，需要手动将模型抽壳至所需壁厚，并将其中填入所需的infill模板
按不同打印层数切片的方式不实际，因为可能产生过大的元素数量，反而导致运算困难。

## Actual Manufacturing

可以通过以下方法进一步提高打印强度：

|Procedures|Theory|
|-|-|
|Increase the printing temperature|Reduce cooling gradient for interlayer fusion connection|
|Sufficient annealing treatment|Make molecular chains better connected and reduce internal stress|
|Minimize the print layer height|Increase interlayer fusion area|
|Enable brick layer slicing|Improve XZ ultimate tensile strength by 5 ~ 10 % during tensile stress test for most filaments|

## Compare To Injection Molding

在相同重量下，3D打印件的强度远无法匹敌注塑件，同时3D打印在耗材选择上也不具有注塑件的灵活性。但3D打印工艺具有可快速设计和快速调整的特性，因此在非受力部件的应用上有绝对优势。以下是两者的一些对比：

|-|3D Printing|Injected Molding|
|-|-|-|
|Material characteristics|Anisotropy|Isotropic *|
|Material Options|Single filament|Multi-ingredient pellet mixable|
|Material Property|Higher thermal / humidity stability|Higher liquidity, Less additive required|
|Material Source|Common plastics<br>(ABS, PETG, PA...)|More specialty plastics<br>(PA-GF, PC, PAEK, PTE...)|
|-|-|-|
|Build Pressure|1 ~ 35 Mpa<br>(Gear extrude)|2 ~ 200 Mpa<br>(Hydraulic screw press)|
|Typical XY Tensile Modulus (GPa)|1.6 ~ 2.2 (x0.8)|2.0 ~ 2.4 (x1.0)|
|Typical XZ Tensile Modulus (GPa)|0.8 ~ 1.3 (x0.4)|Isotropic *|
|Dimensional Accuracy|0.01 ~ 0.3 mm|＜ 0.01 mm|
|-|-|-|
|Design-To-Product Time|In hours|More than weeks|
|Starting Cost|$ 0.25<br>(Electricity and consumables)|$ 1000<br>(Mold design, manufacturing and transportation)|

 \* Controllable depends on different injection point designs. May use with simulator software such as Autodesk Moldflow.

## Uncharted Knowledge

3D printed injection molding 

# Remarks 
