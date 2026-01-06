# BestPractice SimLoad Extremes

組織全体で負荷がどこに集中しているかを把握しやすいよう、各役職の Top / Average / Min を一覧化し、SimLoad（正規化含む）を比較します。

## 概要テーブル

| Role | Type | Node | SimLoad | Normalized | Score | Tasks | Children |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| CXO | Top | CXO_0 | 10706529.10 | 1.000 | 0.77500 | 349938 | 6250 |
| CXO | Average | - | 10706529.10 | 1.000 | 0.77500 | 349938.00 | 6250.00 |
| CXO | Min | CXO_0 | 10706529.10 | 1.000 | 0.77500 | 349938 | 6250 |
| Director | Top | Director_172 | 56193.00 | 0.005 | 0.00370 | 1861 | 1 |
| Director | Average | - | 49809.61 | 0.005 | 0.00328 | 1671.52 | 1.00 |
| Director | Min | Director_5410 | 44161.10 | 0.004 | 0.00291 | 1502 | 1 |
| SeniorManager | Top | SeniorManager_7569 | 118184.50 | 0.011 | 0.00775 | 4727 | 1 |
| SeniorManager | Average | - | 108452.15 | 0.010 | 0.00711 | 4382.18 | 1.00 |
| SeniorManager | Min | SeniorManager_8391 | 98879.20 | 0.009 | 0.00649 | 3959 | 1 |
| Manager | Top | Manager_13819 | 179014.10 | 0.017 | 0.01173 | 13797 | 1 |
| Manager | Average | - | 167250.54 | 0.016 | 0.01096 | 12997.30 | 1.00 |
| Manager | Min | Manager_16849 | 156491.20 | 0.015 | 0.01026 | 12174 | 1 |
| Player | Top | Player_20069 | 112748.00 | 0.011 | 0.00738 | 6998 | 0 |
| Player | Average | - | 105564.69 | 0.010 | 0.00691 | 6599.09 | 0.00 |
| Player | Min | Player_23099 | 99140.00 | 0.009 | 0.00649 | 6198 | 0 |

### CXO

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | CXO_0 | - | CXO_0 |
| SimLoad | 10706529.10 | 10706529.10 | 10706529.10 |
| Normalized | 1.000 | 1.000 | 1.000 |
| Score | 0.77500 | 0.77500 | 0.77500 |
| Tasks | 349938 | 349938.00 | 349938 |
| Children | 6250 | 6250.00 | 6250 |

### Director

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | Director_172 | - | Director_5410 |
| SimLoad | 56193.00 | 49809.61 | 44161.10 |
| Normalized | 0.005 | 0.005 | 0.004 |
| Score | 0.00370 | 0.00328 | 0.00291 |
| Tasks | 1861 | 1671.52 | 1502 |
| Children | 1 | 1.00 | 1 |

### SeniorManager

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | SeniorManager_7569 | - | SeniorManager_8391 |
| SimLoad | 118184.50 | 108452.15 | 98879.20 |
| Normalized | 0.011 | 0.010 | 0.009 |
| Score | 0.00775 | 0.00711 | 0.00649 |
| Tasks | 4727 | 4382.18 | 3959 |
| Children | 1 | 1.00 | 1 |

### Manager

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | Manager_13819 | - | Manager_16849 |
| SimLoad | 179014.10 | 167250.54 | 156491.20 |
| Normalized | 0.017 | 0.016 | 0.015 |
| Score | 0.01173 | 0.01096 | 0.01026 |
| Tasks | 13797 | 12997.30 | 12174 |
| Children | 1 | 1.00 | 1 |

### Player

| 指標 | Top | Average | Min |
| --- | --- | --- | --- |
| Node | Player_20069 | - | Player_23099 |
| SimLoad | 112748.00 | 105564.69 | 99140.00 |
| Normalized | 0.011 | 0.010 | 0.009 |
| Score | 0.00738 | 0.00691 | 0.00649 |
| Tasks | 6998 | 6599.09 | 6198 |
| Children | 0 | 0.00 | 0 |
