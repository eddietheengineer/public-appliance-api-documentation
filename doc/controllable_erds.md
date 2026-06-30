# Controllable ERDs

The following ERDs can be controlled because they have a paired Request and Status ERD.

| Name | Request ERD | Status ERD(s) | HA Domain | Writable | Description |
| ---- | ----------- | ------------- | --------- | -------- | ----------- |
| Eco Mode | 0x1076 | 0x1077 | switch | Yes | Sets eco mode state |
| Allow Auto Water Valve Shut Off | 0x1173 | 0x1174 | switch | Yes | Used to request allowing automatic water valve shut off when an issue is detected. |
| Turbo Cool | 0x120c | 0x100f, 0x120d | switch | Yes | Used to request setting turbo cool mode on or off. |
| Turbo Freeze | 0x121a | 0x100e, 0x121b | switch | Yes | Used to request setting turbo freeze mode on or off. |
| Presence Sensing Enable | 0x1222 | 0x1223 | switch | Yes | Used to request that presence sensing is enabled or disabled. |
| Presence Sensed Activates Recess Light | 0x1224 | 0x1225 | switch | Yes | Request to enable or disable the dispenser recess light turning on when a presence is sensed. |
| Door Alarm Enable | 0x1227 | 0x1228 | switch | Yes | Used to request setting the door alarm enabled or disabled. |
| Night Time Snack Mode Lighting | 0x1229 | 0x122a | switch | Yes | Request to enable or disable night time snack mode. |
| Kitchen Illumination Feature Enable | 0x1255 | 0x1256 | switch | Yes | Request to enable the kitchen illumination feature. |
| Door Alarm Timer Timeout | 0x1258 | 0x1259 | number | Yes | Used to request the desired time before a door alarm is triggered. Maximum time limits are defined in ERD 125A |
| Barcode Scanner Feature | 0x125f | 0x1260 | switch | Yes | Used to request enabling or disabling the barcode scanner |
| Barcode Scanner Device Power | 0x1263 | 0x1264 | switch | Yes | Used to request the barcode scanner device power on or off status |
| Recess Light SBC Brightness | 0x1269 | 0x126a | number | Yes | Request from the SBC to set the light level for dispenser light to a value between 0 and 100 percent. |
| Variable Cube Size | 0x12ba | 0x12bb | number | Yes | Used to request the desired ice cube size. Maximum cube size is defined in ERD 12B9 |
| Fridge Focus Camera Enable | 0x12ec | 0x12ed | switch | Yes | Request to enable or disable the Fridge Focus camera. |
| System Power Off | 0x14c6 | 0x14c7 | switch | Yes | Used to request system power state for specific loads |
| Wash Mode Option | 0x2126 | 0x2127 | switch | Yes | Use this ERD to request a change of ERD 0x2127 Wash option selection. After this ERD is written by a client, it will be updated with an invalid value. |
| Dry Mode Option | 0x2129 | 0x2128 | switch | Yes | Use this ERD to request a change of ERD 0x2128 Dry option selection |
| More Dry Option | 0x213b | 0x213a | switch | Yes | Use this ERD to request a change of ERD 0x213A More Dry option selection. After this ERD is written by a client, it will be updated with an invalid value. Depends on - 0x2000 Machine State must not be Idle or Commissioning. |
| Smart Combi Option | 0x216f | 0x216e | switch | Yes | Use this ERD to request a change of ERD 0x216E smart combi option. |
| Commercial Remote Admin Mode Pin | 0x2237 | 0x2238 | number | Yes | This erd requests a change to the current Admin Mode Pin stored in the unit. |
| Commercial Remote Buzzer Disable | 0x223a | 0x223b | switch | Yes | This erd can request to disable or enable the unit's buzzer. Erd shall show 0xFF when request is consumed. |
| Commercial Remote Wash Water Level | 0x223f | 0x2240 | number | Yes | This erd requests a change to the target wash water level of all the cycles of Commercial FL Washer. |
| Commercial Remote Wash Time In Seconds | 0x2242 | 0x2243 | number | Yes | This erd requests a change to the target wash time in seconds of all the cycles of Commercial FL Washer. |
| Commercial Remote Rinse Water Level | 0x2245 | 0x2246 | number | Yes | This erd requests a change to the target rinse water level of all the cycles of Commercial FL Washer. |
| Commercial Remote Extra Rinse Option Deselected By Default | 0x2248 | 0x2249 | switch | Yes | This erd can request to have the extra rinse option deselected by default in all cycles of the Commercial FL Washer extra rinse option. |
| Commercial Remote Dry Temperature | 0x224f | 0x2250 | number | Yes | This erd requests a change to the dry temperature. This erd uses data in the option order stated in erd 0x2236. Unused entries stated in erd 0x2236 with OptionId_DontCare (0xFF) shall be ignored. |
| Commercial Remote Cooldown Temperature | 0x2255 | 0x2256 | number | Yes | This erd requests a change to the cooldown temperature. This erd uses data in the option order stated in erd 0x2236. Unused entries stated in erd 0x2236 with OptionId_DontCare (0xFF) shall be ignored. |
| Commercial Remote Free Mode | 0x2338 | 0x2339 | select | Yes | This erd requests a change to the unit commercial operating mode. |
| Smart Assist Cloud Notification | 0x310c | 0x310d | switch | Yes | Write to this ERD to set Smart Assist Cloud Notification. This controls the Smart Assist LED on the dishwasher UI for cloud based notifications. The status for this ERD is stored in 0x310D. |
| Custom Cycle Index | 0x322c | 0x322d | number | Yes | This is used to request a custom cycle index from a client. uiCycles <= index < totalCycles (these values are defined in ERD 0x3200). If the custom cycle has not been selected, default value is 255. |
| Clock Display | 0x5019 | 0x501a | switch | Yes | Request clock display to be enabled/disabled. Acceptance of write can be read in ERD 0x501A. |
| Enhanced Sabbath Cooking Accepted | 0x502f | 0x5030 | switch | Yes | This ERD is used to accept/cancel an Enhanced Sabbath/Holiday cook mode, given the current Enhanced Sabbath State (ERD 0x502E). 1. To to accept the cooking prompt, set this ERD to true while the State is 'Prompt Sabbath' (1) or 'Prompt Holiday' (2). (State will become 'Cooking Accepted, Sabbath Pending' (3) or 'Cooking Accepted, Holiday Pending' (4), respectively.) 2. To revoke acceptance, set this ERD to false while the the State is 'Cooking Accepted, Sabbath Pending' (3) or 'Cooking Accepted, Holiday Pending' (4). (State will revert to 'Prompt Sabbath' (1) or 'Prompt Holiday' (2), respectively.) 3. To cancel an active Sabbath/Holiday cook mode, set this ERD to false while the the State is 'Sabbath Active, Warm' (7), 'Holiday Active, Warm' (8), or 'Holiday Active, Bake' (9). (State will become 'Sabbath Active, No Cooking' (5) or 'Holiday Active, No Cooking' (6), resepctively.) The client is responsible for resetting this ERD to false after the Sabbath/Holiday period ends. See status ERD 0x5030. |
| Enhanced Sabbath Warmness Setting | 0x5031 | 0x5032 | switch | Yes | Request to set the warmness level for Enhanced Sabbath warm cycles. See status ERD 0x5032. |
| Cook Cam AI Assistant Enabled | 0x504e | 0x504f | switch | Yes | Writing to this ERD will request to change the state of the Cook Cam AI Assistant feature. See ERD 0x504F for the Cook Cam AI Assistant Enabled Status. |
| Cook Cam Image Upload Enabled Setting | 0x5053 | 0x5054 | switch | Yes | User setting to enable or disable cook cam image uploads to the cloud. User consent is required. Client should request settings updates via this ERD. |
| Upper Oven Do Not Stop Cook Mode On Timer Expiration | 0x511a | 0x511b | number | Yes | Requests whether the cook mode should end when the timer expires in the upper oven. |
| Lower Oven Do Not Stop Cook Mode On Timer Expiration | 0x521a | 0x521b | number | Yes | Requests whether the cook mode should end when the timer expires in the lower oven. |
| Energy Conservation | 0x7052 | 0x7054 | select | Yes | A configurable-level of Eco Energy Savings. This applies to any running mode. |
| Fan Configuration in Cooling | 0x7451 | 0x7450 | select | Yes | The client will request a change to how the indoor fan operates when the appliance is in local control and in cooling mode |
| Fan Configuration in Heating | 0x7453 | 0x7452 | select | Yes | The client will request a change to how the indoor fan operates when the appliance is in local control and in heating mode |
| Freeze Sentinel | 0x7455 | 0x7454 | switch | Yes | The client will request a change Freeze Sentinel status |
| Heat Sentinel | 0x7457 | 0x7456 | switch | Yes | The client will request a change the Heat Sentinel status |
| Constant Fan | 0x7459 | 0x7458 | switch | Yes | The client will request a change to the Constant Fan status |
| 24V External Thermostat | 0x745b | 0x745a | switch | Yes | The client will request a change to the 24V External Thermostat Enabled Status |
| Fan Boost | 0x745d | 0x745c | switch | Yes | The client will request a change to the Fan Boost status |
| Heat Selector | 0x745f | 0x745e | select | Yes | The client will request a change to the Heat Selector status |
| UVC Module | 0x7463 | 0x7462 | switch | Yes | The client will request a change to UVC Module status. |
| Make-up Air Fan Cfm | 0x7465 | 0x7464 | number | Yes | The client will request a change to Make-up Air Fan Cfm status. When the request is consumed, the device will set this Erd to 0xFFFF |
| Make-up Air Filter Type | 0x7467 | 0x7466 | select | Yes | The client will request a change to the Make-up Air Filter Type status |
| Make-up Air Occupancy Control | 0x7469 | 0x7468 | switch | Yes | The client will request a change to the Make-up Air Occupancy Control status. |
| Dehumidification Mode | 0x746b | 0x746a | select | Yes | The client will request a change to the Dehumidification Mode status |
| Heat Pump Lockout Temperature | 0x746f | 0x746e | number | Yes | The device will publish the current Heat Pump Lockout Temperature and the limits for this value |
| Input Current Limiting | 0x7471 | 0x7470 | number | Yes | The client will request a change to the Input Current Limiting status. |
| Heat Source Optimization | 0x7473 | 0x7472 | select | Yes | The client will request a change to the Heat Source Optimization status. |
| Power | 0x7701 | 0x7700 | switch | Yes | The client can request a change to the Power Enabled status. Whether or not the request was accepted, the appliance resets this Erd to 0xFF as an indication the request was 'consumed' and have it ready for the next request. |
| System Mode | 0x7703 | 0x7702 | select | Yes | The client can request a change to the System Mode Status. Only System Modes that the device supports will be accepted. Whether or not the request was accepted, the appliance resets this Erd to 0xFF as an indication the request was 'consumed' and have it ready for the next request. |
| User Heating Setpoint | 0x7707 | 0x7706 | number | Yes | The client can request a change to the User Heating Setpoint. Only User Heating Setpoints that the device allows will be accepted. Whether or not the request was accepted, the appliance resets this Erd to 0x7FFF as an indication the request was 'consumed' and have it ready for the next request. |
| User Cooling Setpoint | 0x770a | 0x7709 | number | Yes | The client can request a change to the User Cooling Setpoint. Only User Cooling Setpoints that the device allows will be accepted. Whether or not the request was accepted, the appliance resets this Erd to 0x7FFF as an indication the request was 'consumed' and have it ready for the next request. |
| Heat System Mode Fan Setting | 0x7719 | 0x7718 | select | Yes | The client can request a change to Fan setting that the appliance uses when in Heat System Mode. Only Fan settings that the device allows will be accepted. Whether or not the request was accepted, the appliance resets this Erd to 0xFF as an indication the request was 'consumed' and have it ready for the next request. |
| Fan System Mode Fan Setting | 0x771c | 0x771b | select | Yes | The client can request a change to Fan setting that the appliance uses when in Fan System Mode. Only Fan settings that the device allows will be accepted. Whether or not the request was accepted, the appliance resets this Erd to 0xFF as an indication the request was 'consumed' and have it ready for the next request. |
| Cool System Mode Fan Setting | 0x771f | 0x771e | select | Yes | The client can request a change to Fan setting that the appliance uses when in Cool System Mode. Only Fan settings that the device allows will be accepted. Whether or not the request was accepted, the appliance resets this Erd to 0xFF as an indication the request was 'consumed' and have it ready for the next request. |
| Dehumidifier Nonstop Mode | 0x7833 | 0x7834 | switch | Yes | Request for the dehum to enter nonstop mode. |
| Turbo/Quiet Mode Modifier | 0x795e | 0x7963 | select | Yes | Request to set which Mode modifier, Turbo/Quiet, is selected. |
| External Damper | 0x7974 | 0x7973 | switch | Yes | External Damper ON/OFF Control |
| Temperature Display Mode Selection | 0x7980 | 0x7981 | select | Yes | Overrides the user selected mode for displaying temperature. Temperature can be selected to represent the set-temperature or ambient-temperature. |
| Filter Replacement Interval Reminder | 0x79a0 | 0x79a1 | number | Yes | Request to Change User-Selectable reminder interval, in hours, for a filter change. |
| Auto Mode Temperature Deadband | 0x79aa | 0x79a9 | number | Yes | Request to change the width of the Auto Mode Temperature Deadband, in degrees F. |
| Compressor Minimum Runtime | 0x79ac | 0x79ab | number | Yes | Requests to change the Minimum Runtime, in minutes, for the Compressor. |
| Compressor Minimum Idle Time | 0x79ae | 0x79ad | number | Yes | Requests to change the Minimum Idle Time, in minutes, for the Compressor |
| Compressor Maximum Stage1 Runtime | 0x79b0 | 0x79af | number | Yes | Requests to change the Maximum Stage1 Runtime, in minutes, for the Compressor. |
| Fan Operating Mode | 0x79be | 0x79bd | select | Yes | Request to change Fan Operating Mode for third party unitary |
| Indoor Temperature Chassis/Install Adjustment | 0x79c1 | 0x79c0 | number | Yes | Sets the Ambient Temperature adjustment that should be performed on 0x7A02 to account for Chassis or Install situation |
| Compressor Minimum Stage2 Temperature Delta | 0x79c4 | 0x79c3 | number | Yes | Requests to change the Minimum Stage2 Temperature Delta, in degrees F, for the Compressor. |
| Blower Minimum Runtime | 0x79c6 | 0x79c5 | number | Yes | Requests to change the Minimum Runtime, in minutes (X10), for the Blower |
| Indoor Fan Delay | 0x79c8 | 0x79c7 | number | Yes | Requests to change the Delay, in minutes (X10), for the Indoor Fan |
| Minimum Heat Time | 0x79ca | 0x79c9 | number | Yes | Requests to change the Minimum Heat Time, in minutes, for the System. |
| Auxiliary Heat Minimum Temperature Delta | 0x79cc | 0x79cb | number | Yes | Requests to change the Minimum Temperature Delta, in degrees F (X10), for Auxiliary Heat. |
| Indoor Ambient Temperature Sensor Calibration | 0x79ce | 0x79cd | number | Yes | Requests to change the Calibration, in degrees F (X10), for the Indoor Ambient Temperature Sensor. |
| Smoke | 0x9404 | 0x9403 | switch | Yes | The request to enable smoke |
| Early Completion Notification Temperature Threshold | 0x942c | 0x942b | number | Yes | The requested early completion notification temperature threshold setting. The early completion notification based on temperature is triggered when: * Actual probe temperature >= Probe target temperature - Early Completion Notification Temperature Threshold. If the threshold entered by the user is in Celsius then: * ERD Value in (F) = User Entered Value (C) x 9/5  (Rounded to the closest integer). |
| Early Completion Notification Time Threshold | 0x942f | 0x942e | number | Yes | The requested cook time remaining value when the early completion notification is triggered. |
| Temperature Offset | 0x9503 | 0x9502 | number | Yes | The requested value of temperature offset setting |
| Temporary Temperature Offset Demand Response | 0xd00b | 0xd00c | number | Yes | Specifies the parameters for a Temperature Offset Demand Response Event |
| Cost of power cost/comfort slider | 0xd00e | 0xd00f | number | Yes | This allows the client to balance cost savings against comfort in the form of stable water temperature A value of 0 will allow full cost savings, which will vary the water heater tank setpoint and charging times in order to maximize use of off-peak power and reduce or eliminate peak priced power. A value of 255 will prioritize temperature setpoint stability at the expense of sometimes using peak priced power. Values between 0 and 255 give a sliding scale of temperature stability vs cost savings |

*Total: 85 controllable ERDs*
