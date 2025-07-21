<!--Chinese language comparison included 包含汉语对照-->
# Status 

Draft

# Project Description

由于Quiver项目长期以来使用3D打印方法制作原型和部分产品的结构件，但缺乏对其强度的具体研究，且最初级的FEA（有限元分析）工作流程仅适用于均质部件，无法为3D打印件提供可靠结果。为了解决这个问题，现决定收集并整理一些学术知识，以增进我们对3D打印结构的了解，并在成本可控的前提下改良我们的3D打印结构设计流程。

同时，将收集一些注塑相关的参数，与3D打印件进行比较。

# Methodology 

将结合过往的3D打印操作经验，并在网络上搜索和整理相关的研究成果和论文，同时将收集到的文章和标准交由AI助手ChatGPT-O3进行交叉比对。必要时将使用Inventor或Fusion进行实操和求解。

# Results and Deliverables 

## Overview

通常3D打印（增材制造）部件无法通过使用均质参数的FEA得出正确结果，在宏观方面有以下主要原因：

1. 各类不同的层厚、壁厚和infill密度设计，会直接影响力在部件内的传递。
2. 层内的耗材分子连接连续性好，就像玻璃受热相变后又冷凝为单体。而层间则为强度较弱的二次熔融扩散连接，就像两块一经解冻又再次冷冻在一起的肉，外壁相互之间粘合。这个特征导致部件的XY（层内）与XZ（层间）方向之间强度差别巨大。

这些特性致使3D打印件需要使用正交各向异性的FEA方法来求解，并且各种不同的密度和填充参数均需要定制不同的工作流程。总而言之，相对于均质部件，3D打印部件的FEA流程实际上变化多样。

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
1. 从厂家的参数表获得 
2. 使用兼容的Tensile testing machine
3. 两者需要配合使用

不像均质和各向同性FEA，正交各向异性FEA所需的参数更多，我们需要准备以下耗材丝参数用于：

### From Manufacturer's parameter card

|Item|Symbol (Unit)|Actual Possible Situation|
|-|-|-|
|Density of fresh filament|ρ (g/cm3)|Usually provided perfectly|
|Young's (Tensile) modulus|(Mpa)||
|... X|Ex|Usually provided|
|... Y|Ey|Direction of parallel tracks are almost impossible to control,<br>usually no Y data provide|
|... Z|Ez|Usually provided|
|Tensile strength|(Mpa)||
|... X|σx|Usually provided|
|... Y|σy|Direction of parallel tracks are almost impossible to control,<br>usually no Y data provide|
|... Z|σz|Usually provided|
||||
||||
||||
||||


对于声誉良好且测试环节完善的3D打印耗材丝制造商，通常我们可以在其商品页面找到对应材料的性能表或文档，例如：

|BASF Ultrafuse® PLA|BambuLab|
|-|-|
|||

### From Tensile Testing Machine Result

TBD 对于缺乏的参数，需要打印以下测试条，并以实测的方式获取参数：

|Standard Name|Specimen|Method|Purpose|
|-|-|-|-|
|ISO 527-2|ASTM D638|Tensile testing by pulling apart|Get Young's modulus / Tensile modulus|
|ISO 178|ASTM D790|Flexural or bending testing by press on center||
|ISO 179-2|ASTM D6110|Charpy impact testing by strike on other side of the notch||

## Shape Preparation

TBD 正确的切片方式？

在使用FEA求解前，需要手动将模型抽壳至所需壁厚，并将其中填入所需的infill模板。
按不同打印层数切片的方式不实际，因为可能产生过大的元素数量，反而导致运算困难。

TBD 模型的UCS定向？

按3D打印的常规理解方式，垂直方向即为正交的Z轴。

TBD 每个元素的细分精度和预计需要的时间？

## Additional Tip For Actual 3D Printing Manufacturing

如果FEA结果与测试差异过大（＞ 20 %）或因其他某些原因导致FEA结果无法确信，可以通过以下方法尝试提高打印强度：

|Procedures|Theory|
|-|-|
|**Design**||
|Use 1.5 ~ 2 times of wall thickness|Increase interlayer connection strength|
|Double the amount of corner braces and reinforce beams|Directly improve overall strength|
|Use chamfered corner design more often|Increase the bending strength around corners|
|**Slicing**||
|Use better force spreading infill patterns|Disperse the load force into different directions or other fasteners|
|Optimizing print direction|Avoid shear and tension between layers by rotate the slicing|
|Enable brick layer slicing|Improve XZ ultimate tensile strength by 5 ~ 10 % during tensile stress test for most filaments|
|**Printing**||
|Increase the nozzle and chamber temperature|Reduce cooling gradient for interlayer fusion connection|
|Reduce cooling effect|Make molecular chains of fresh extruded traces better connecting between neighbor traces|
|Minimize the print layer height|Increase interlayer fusion area|
|**Post Processing**||
|Sufficient annealing treatment|Make molecular chains better connecting in all direction and release internal stress|
|Epoxy resin infill|Simulating the effect of reinforced concrete by taking advantage of the hollow nature of 3D printing|

## Compare To Other Technologies

### Vs Injection Molding

众所周知，在相同重量下且无论经过何种加工，且无论是否使用工业级设备，常见的FDM(Fused Deposition Modeling)3D打印件的强度远无法匹敌注塑件，同时3D打印在材料选择上也不具有注塑件的灵活性。但FDM 3D打印工艺具有可快速设计、快速迭代的特性，因此在非受力部件的应用上有绝对优势，这又是注塑无法比拟的。以下是两者的一些对比：

（所有数值均使用ABS材料的典型值）

|-|FDM 3D Printing|Injection Molding|
|-|-|-|
|Material characteristics|Orthotropic|Isotropic *|
|Material Customize|Single filament|Multi-ingredient pellet mixable|
|Material Property|Higher thermal / humidity stability|Higher liquidity, Less additive required|
|Material Source|Common plastics<br>(ABS, PETG, PA...)|More specialty plastics<br>(PEI, PC, PAEK, PTE...)|
|-|-|-|
|Build Pressure|1 ~ 35 Mpa<br>(Gear extrude)|2 ~ 200 Mpa<br>(Hydraulic screw press)|
|XY Tensile Modulus (GPa)|1.6 ~ 2.2 (x0.8)|2.0 ~ 2.4 (x1.0)|
|XZ Tensile Modulus (GPa)|0.8 ~ 1.3 (x0.4)|Isotropic *|
|XY Tensile Strength (MPa)|32 ~ 42 (x0.8)|40 ~ 50 (x1.0)|
|XZ Tensile Strength (MPa)|12 ~ 22 (x0.3)|Isotropic *|
|-|-|-|
|Dimensional Accuracy (mm)|0.01 ~ 0.3|≤ 0.01|
|Design-To-Product Time|In hours|More than weeks|
|Starting Cost|$ 0.25<br>(Electricity and filament consume)|$ 1000<br>(Mold design, manufacturing and transportation)|

 \* Controlled by different injection point designs. May perform simulator with Autodesk Moldflow or similar software.

 ### Vs Other Advanced 3D Printing Technology 

 TBD 需要加入铝和不锈钢等金属SLS 3D打印件的参数以对比，尤其是造价部分

 但是，实际上其他更先进的3D打印技术已经在逐渐逼近注塑级强度，同时还有着远比注塑更加低廉的成本。以下是一些对比：

 (所有数值均使用PA12材料的典型值，且PA12具有一定韧性）

 |-|FDM<br>(Fused Deposition Modeling)|SLS<br>(Selective laser sintering)|MJF<br>(Multi Jet Fusion)|
 |-|-|-|-|
 |Material characteristics|Orthotropic|80 ~ 90 % Isotropic|95 ~ 98% Isotropic|
 |Material Customize|Single filament|Dyeable, Aluminum mixable|Dyeable|
 |Material Property|Higher thermal / humidity stability|Higher liquidity, Less additive required|
 |Material Source|All common 3d printing materials|PA11, PA12, PA12-GF, PP, TPU|PA11, PA12, PA12-GF, TPU|
 |-|-|-|-|
 |Raw Material Density (g/cm3)|1.05|0.93|1.01|
 |XY Tensile Strength (MPa)|≈ 32|44 ~ 50|48 ~ 52|
 |XZ Tensile Strength (MPa)|≈ 18|80 ~ 90 % Isotropic|95 ~ 98% Isotropic|
 |-|-|-|-|
 |Starting Cost|$ 0.25|$ 10|$ 8|
 

## Questions & Uncharted Knowledge

- 3D打印件本身是否可以衍生设计作为模具使用？是否可以承受模具所受的温度和压力？
- 是否有可靠的化学凝固的方式可以作为注塑的下位替代品？例如环氧树脂水晶滴胶或光敏树脂？
- 是否可以通过喷涂强化涂料来增加3D打印件外壁强度？
- 是否有小批量且低成本的注塑工艺流程？

# Remarks 
