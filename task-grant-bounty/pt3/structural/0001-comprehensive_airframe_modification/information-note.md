[Chinese language comparison included 包含汉语对照]: #
# Status 

Draft

# Project Description

为了实现Quiver下一阶段的PT3计划中的功能，决定在PT2至PT3的升级工作中，对cockpit区域的外壳、GNSS模块安装方式、attachment interface和高度计安装方式进行大幅度改良：

- Enclosure Assembly：由于PT2的主体结构为铝板框架，且电源和航电区域的外壳仅具有较低的防护面积和等级。因此决定设计一套新的外壳，同时对原有的部分外壳进行升级改造，以满足其对关键设备区域的防护性能。
- GNSS Stand：经过多次讨论决定，RTK-GNSS模块将安装在机身内，但需要探索新的安装方式，因此设计了一个GNSS stand。
- Attachment Interface：attachment interface由1个增加为3个，同时所有attachment interface均添加了延伸结构，以强化人机工效。
- Altimeter Mounting Frame：设计了集成安装支架，以重新整合LiDAR和无线电高度计的安装布局。

# Methodology 

本次设计和交付均使用Fusion 360软件，所有的新设计均基于Julius所设计的PT2 airframe、Main PCB、Battery connector PCB和各类外部导入的零部件的3d模型。

## Enclosure Assembly

外壳使用了各种设计以防止雨水溅入、滴落或渗入电子设备区域。Enclosure Assembly分为4个部分，分别为：Battery PCB enclosure、Main enclosure、Front lid和Top cap。

- 在需要与各类电子设备交互的开口部分使用了雨檐设计和防滴落设计，而外壳的缝隙和边缘采用了具有反坡坡度的防渗水设计。
- 为power connector PCB设计了新的外壳，具有现有更好的散热和对PCB的支撑作用，同时尽量减轻了非受力部分的结构重量。
- Main enclosure的一侧设有为telemetery天线预留的RP-SMA连接器安装支架。
- Top cap则延续了PT2的铰链开合的功能，并重新设计了整个外形和体积，以满足机身内GNSS接收机的净空需求。

更多详情请见model space内的具体设计细节。

## GNSS Stand

- GNSS接收机被置于FCU上方约2厘米的位置以降低EMI干扰，为此布局专门设计了一个新的拱门式支架，得以使GNSS模块在不直接接触FCU和其PCB的条件下达成稳定支撑。
- GNSS stand分为支架和紧固框架，支架为主体结构，紧固框架用于将GNSS接收机的PCB夹在主体结构上。

## Attachment Interface

- 在机身两侧各新增了一个attachment interface。同时对vertical plate进行了改动，闭合了中央的减轻孔，并在其原有位置上增加了attachmen interface所需的螺丝孔位和线缆开口。
- 在底部attachment interface的延伸结构上设计了侧向的线缆开口，且开口处具有防刮蹭和防雨水沿线缆渗入的设计。
- 考虑到便于任务设备的拆装和更换，所有attachment interface现在均安装在新设计的延伸支架上，延伸长度为3cm，以增加其与机身之间的净空距。

## Altimeter Mounting Frame

在引用并调整了两个高度计的3d模型并调整了位置后，基于其新位置设计了高度计安装支架。

- 高度计支架包含了一个理线槽，可在一定程度上限制高度计和底部attachment interface的线缆位置，以防止线缆移动并阻挡LiDAR。
- 新的高度计需要在attachment plate上钻出一新的孔位以完成安装。

# Results and Deliverables 

主要成果为：
- 多个新部件的3d模型，以供3d打印，部分新零件在打印时需要使用支撑功能。
- 部分旧的airframe金属部件需要钻孔或重新定制。

# Remarks 
