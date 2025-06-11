[Chinese language comparison included 包含汉语对照]: #
# Status 

Draft

# Project Description

为了满足PT3的预定功能，决定在PT2至PT3的升级计划中，对cockpit区域、GNSS模块安装方式、attachment interface和高度计安装方式进行大幅度改良。
- 由于PT2的主体结构为铝板框架，且电源和航电区域的外壳仅具有较低的防护面积和等级。因此决定设计一套新的外壳，同时对原有的部分外壳进行升级改造，以满足关键设备区域防泼溅的性能。
- 经过讨论决定，RTK-GNSS模块计划安装在机身内，但需要探索新的安装和固定方式。
- attachment interface由1个增加为3个，新增的两个位于battery bay的机身外侧，同时所有attachment interface均添加了延伸结构，以便于任务设备的拆装和更换。
- 设计了集成安装支架，以重新整合LiDAR和无线电高度计的安装布局。

# Methodology 

使用Fusion 360软件
- 防护外壳的各个设备交互开口部分使用了雨檐设计，而缝隙和边缘采用了有坡度的设计，以防止雨水溅入、滴落或渗入设备区域。Top cap则延续了PT2的铰链开合的功能，并重新设计了整个外形和体积，以满足机身内
GNSS接收机的净空需求。
- GNSS接收机被置于FCU上方约2厘米的位置。此布局使用了一个新设计的拱门式支架，得以使GNSS模块在不直接接触FCU和其PCB的条件下达成稳定支撑。
- 底部attachment interface延伸结构上设计了线缆开口，开口处具有防刮蹭和防雨水沿线缆渗入的导水设计。
- 高度计支架有理线区域，可在固定线缆同时防止线缆移动并阻挡LiDAR。

# Results and Deliverables 

主要成果为多个3d模型，并供3d打印（部分需要使用支撑）

# Remarks 
