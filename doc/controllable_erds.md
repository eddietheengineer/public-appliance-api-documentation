# Controllable ERDs

The following ERDs can be controlled because they have a paired Request and Status ERD.

| Name | Request ERD | Status ERD(s) | HA Domain | Writable | Description |
| ---- | ----------- | ------------- | --------- | -------- | ----------- |
| Reset Board | 0x0032 | — | button | Yes | When this ERD changes, the board will reset after the number of seconds specified in the data. After reset the value of this ERD is 255 to enable ERD change detection therefore 255 as a reset value is unsupported. |
| Enhanced Sabbath Mode | 0x004f | — | binary_sensor | Yes | Specifies whether Enhanced Sabbath Mode is active. |
| Nighttime Snack Mode | 0x101e | — | binary_sensor | Yes | Nighttime Snack Mode feature is turned on or off. |
| Lock out feature state | 0x102c | — | binary_sensor | Yes | Used to update the lock out feature state. |
| Display always on feature | 0x102d | — | binary_sensor | Yes | Used to force the display to be on all the time |
| Door Mute Status Upper Compartment | 0x1032 | — | binary_sensor | Yes | Door mute functionality, upper compartment. |
| Door Mute Status Lower Compartment | 0x1033 | — | binary_sensor | Yes | Door mute functionality, lower compartment. |
| Door Mute Status Middle Compartment | 0x1034 | — | binary_sensor | Yes | Door mute functionality, middle compartment. |
| Water Filter Reset | 0x1041 | — | button | Yes | Request that the water filter timer be reset |
| Autofill pitcher feature | 0x1053 | — | binary_sensor | Yes | Request to enable or disable autofill pitcher feature |
| Eco Mode | 0x1076 | 0x1077 | switch | Yes | Sets eco mode state |
| Water Filter Reset | 0x1166 | — | button | Yes | Set to trigger water filter reset. |
| Valve Manual Override | 0x1168 | — | binary_sensor | Yes | Indicates valve is in manual override state.  Must be cleared before a valve position command accepted. |
| Unlock | 0x116f | — | binary_sensor | Yes | Triggers Unlock of Go Box. (resets to 0 after request serviced). |
| Allow Auto Water Valve Shut Off | 0x1173 | 0x1174 | switch | Yes | Used to request allowing automatic water valve shut off when an issue is detected. |
| Turbo Cool | 0x120c | 0x120d | switch | Yes | Used to request setting turbo cool mode on or off. |
| Turbo Freeze | 0x121a | 0x121b | switch | Yes | Used to request setting turbo freeze mode on or off. |
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
| SBC Request To Power Off Barcode Scanner | 0x142c | — | binary_sensor | Yes | Used by the SBC to request powering the barcode scanner off |
| Variable Cube Size Request 0 | 0x14be | — | number | Yes | Used to request the desired ice cube size. Maximum cube size is defined in ERD 14BD |
| Variable Cube Size Request 2 | 0x14c1 | — | number | Yes | Used to request the desired ice cube size. Maximum cube size is defined in ERD 14C0 |
| Dimmable Lighting 0 Warmth Percentage | 0x14c3 | 0x14c4 | number | Yes | Request to set the warmth percentage for lights to a value between 0 and 100 percent. |
| System Power Off | 0x14c6 | 0x14c7 | switch | Yes | Used to request system power state for specific loads |
| Legacy - Dryer Extended Tumble Selection | 0x201b | — | binary_sensor | Yes | Specifies Extended Tumble selection. Notes: - This is really a legacy ERD and in the past was not a member of any API. - It has recently been added to an API to be future compatible. - Maintained for Legacy App Versions - In legacy units - writing to this ERD will set the ExtendedTumble Selection - Modern units maintain this ERD for compatibility with Legacy Apps - writing to this ERD will send a request for this change to 0x2051 Extended Tumble Option Request - if enable request is granted then a request is sent to disable EcoDry via 0x2044 EcoDry Option Request - 0x201B Dryer Extended Tumble Selection is maintained to match 0x2053 Extended Tumble Option Selection - Prefer using the Extended Tumble API |
| Remote Stop Cycle | 0x2040 | — | binary_sensor | Yes | Write zero to this ERD to stop the currently running, paused, delay run or delay paused cycle. Depends on: - ERD 0x2000 must be Run, Pause, Delay Run or Delay Pause - ERD 0x2039 must be Enabled ERD 0x2040 is a member of - API V1 Remote Start and Stop and - API V2 Remote Start and Stop V2. API V2 Remote Start and Stop V2 takes precedence. |
| Remote Start Extended Tumble | 0x2041 | — | binary_sensor | Yes | Write zero to this ERD to start the Extended Tumble part of the current selected cycle. Depends on - ERD 0x2000 must be Idle, Standby, or End Of Cycle - ERD 0x2039 must be Enabled. API V2 Remote Start and Stop V2 takes precedence. |
| Time Saver Option | 0x2054 | — | binary_sensor | Yes | This ERD is used to request a change of the Time Saver option, a feature that allows a user to select a shorter wash cycle. |
| Steam Option | 0x2057 | — | binary_sensor | Yes | This ERD is used to request a change of the steam option. |
| Tumble Care Option | 0x2060 | — | binary_sensor | Yes | This ERD is used to request a change of the tumble care option. |
| Wash And Dry Option | 0x2063 | — | binary_sensor | Yes | This ERD is used to request a change of the Wash and Dry option, where a wash cycle is followed by a cycle to dry small loads of laundry. |
| Load Recommended Washer Link Cycle | 0x206a | — | binary_sensor | Yes | Write 255 to this 0x206A to load the cycle in 0x206B Recommended Washer Link Cycle. The ERD will reset back to normal automatically after writing. Depends on - 0x206C Washer Link Option Selection must be Enabled 0x2096 Load Recommended Washer Link Cycle Request is a member of both - V1 Washer Link and - V1 Washer Link 2 |
| Air Fluff Cycle Option | 0x208a | — | binary_sensor | Yes | Use this ERD to request a change of ERD 0x2089 Air Fluff option selection. When a request has been processed, the unit will update this value to 0xFF. |
| Warm Up Cycle Option | 0x2090 | 0x208f | switch | Yes | This erd requests a change in the warm up cycle option status. When a request has been processed, the unit will update this value to 0xFF. |
| Smart Vent Cycle Option | 0x2093 | — | binary_sensor | Yes | This ERD requests a change in the smart vent cycle option status. When a request has been processed, the unit will update this value to 0xFF. Depends on - 0x2094 Smart Vent Cycle Option Allowables |
| Remote Care Start Command | 0x209d | — | binary_sensor | Yes | Writing to this byte will start the current cycle. |
| Color Keeper Option | 0x20a0 | — | binary_sensor | Yes | Request a change of the Color Keeper option. This feature will modify wash cycle parameters to save color in garments. |
| No Tangle Wash Option | 0x20a3 | — | binary_sensor | Yes | Request a change of no tangle wash option. |
| Remote Cycle Selection | 0x20a7 | — | select | Yes | Erd used to request a cycle to be selected by an appliance. - After being written, this ERD value is reset to 0xFF. - If the request is granted, the currently selected cycle is reflected in 0x200A Laundry Current Selected Cycle. |
| True Rinse Option | 0x20a9 | — | binary_sensor | Yes | Request a change of the True Rinse option, which is a feature that improves rinse performance. |
| Delay Wash Option | 0x20b2 | — | binary_sensor | Yes | Used to request a change for delay wash option. |
| Extra Rinse Option | 0x20b4 | — | binary_sensor | Yes | Used to request a change for the extra rinse option. After this ERD is written by a client, it will be updated with an invalid value. |
| Fabric Softener Option | 0x20b6 | — | binary_sensor | Yes | Used to request a change for fabric softener option. |
| Warm Rinse Option | 0x20bd | — | binary_sensor | Yes | Used to request a change for the warm rinse option. |
| Downloaded Cycle | 0x20d1 | — | select | Yes | Used to request a downloaded cycle that users can select via cloud (i.e. app). - After being written, this ERD value is reset to 0xFF. - If the request is granted, the currently downloaded cycle is reflected in 0x20D3. |
| Active Intelligent Option | 0x2116 | 0x2115 | switch | Yes | Request a new active intelligent option |
| Eco Option | 0x2125 | — | binary_sensor | Yes | This ERD requests a change in the Eco Option. |
| Wash Mode Option | 0x2126 | 0x2127 | switch | Yes | Use this ERD to request a change of ERD 0x2127 Wash option selection. After this ERD is written by a client, it will be updated with an invalid value. |
| Dry Mode Option | 0x2129 | 0x2128 | switch | Yes | Use this ERD to request a change of ERD 0x2128 Dry option selection |
| Remote Sensored Dry Only Cycle Start Command | 0x2133 | — | binary_sensor | Yes | Write zero to this ERD to start the Sensor Dry only cycle. Depends on - ERD 0x2000 must be End Of Cycle - ERD 0x2039 must be Enabled. |
| More Dry Option | 0x213b | 0x213a | switch | Yes | Use this ERD to request a change of ERD 0x213A More Dry option selection. After this ERD is written by a client, it will be updated with an invalid value. Depends on - 0x2000 Machine State must not be Idle or Commissioning. |
| Remote Start Selected Cycle | 0x2149 | — | binary_sensor | Yes | Client only can write into this ERD once the Remote Start Allowable Status (0x214A) is enabled. |
| Soaking Rinse Option | 0x214c | — | binary_sensor | Yes | This ERD requests a change in the Soaking Rinse Option. |
| Wash complete cycle notification option | 0x2156 | — | binary_sensor | Yes | Use this ERD to request a change of the 0x2155 Wash complete cycle notification option. After being written, this ERD is invalidated by changing it to an undefined value. |
| Smart Combi Option | 0x216f | 0x216e | switch | Yes | Use this ERD to request a change of ERD 0x216E smart combi option. |
| Reset Current Coin Box Count | 0x2171 | — | button | Yes | This erd requests a change to the coin box coin count. Upon request, the device will clear the coins counted since last opening reported in 0x216A. The device shall write the value of this ERD to request consumed once the coin count has been reset. |
| Smart Wash And Rinse Option | 0x2172 | — | binary_sensor | Yes | Request a change of the smart wash and rinse option. |
| Additional Cavity Remote Stop Cycle | 0x2208 | — | binary_sensor | Yes | Write zero to this ERD to stop the currently running, paused, delay run or delay paused additional cavity cycle. Depends on: - ERD 0x2200 must be run, pause, delay run or delay pause. - ERD 0x2207 must be enabled. |
| Additional Cavity Remote Cycle Selection | 0x2209 | — | select | Yes | ERD used to request a cycle to be selected by an appliances. After being written, this ERD's value is reset to 0xFF and the currently selected cycle is reflected in 0x2203. |
| Commercial Remote Admin Mode Pin | 0x2237 | 0x2238 | number | Yes | This erd requests a change to the current Admin Mode Pin stored in the unit. |
| Commercial Remote Buzzer Disable | 0x223a | 0x223b | switch | Yes | This erd can request to disable or enable the unit's buzzer. Erd shall show 0xFF when request is consumed. |
| Commercial Remote Wash Water Level | 0x223f | 0x2240 | number | Yes | This erd requests a change to the target wash water level of all the cycles of Commercial FL Washer. |
| Commercial Remote Wash Time In Seconds | 0x2242 | 0x2243 | number | Yes | This erd requests a change to the target wash time in seconds of all the cycles of Commercial FL Washer. |
| Commercial Remote Rinse Water Level | 0x2245 | 0x2246 | number | Yes | This erd requests a change to the target rinse water level of all the cycles of Commercial FL Washer. |
| Commercial Remote Extra Rinse Option Deselected By Default | 0x2248 | 0x2249 | switch | Yes | This erd can request to have the extra rinse option deselected by default in all cycles of the Commercial FL Washer extra rinse option. |
| Commercial Remote Dry Temperature | 0x224f | 0x2250 | number | Yes | This erd requests a change to the dry temperature. This erd uses data in the option order stated in erd 0x2236. Unused entries stated in erd 0x2236 with OptionId_DontCare (0xFF) shall be ignored. |
| Commercial Remote Cooldown Temperature | 0x2255 | 0x2256 | number | Yes | This erd requests a change to the cooldown temperature. This erd uses data in the option order stated in erd 0x2236. Unused entries stated in erd 0x2236 with OptionId_DontCare (0xFF) shall be ignored. |
| Commercial Remote Free Mode | 0x2338 | 0x2339 | select | Yes | This erd requests a change to the unit commercial operating mode. |
| Short Cycle Option | 0x2f1b | — | binary_sensor | Yes | Request a change of the Short Cycle option. This feature will modify wash cycle time. |
| Rinse Aid Option State | 0x3101 | — | binary_sensor | Yes | The current state of the Rinse Aid Option State |
| Door Pocket Light State | 0x3108 | — | binary_sensor | Yes | The current state of the door pocket light state |
| Demo Mode State | 0x3109 | — | binary_sensor | Yes | The current state of the Demo Mode state |
| Smart Assist Cloud Notification | 0x310c | 0x310d | switch | Yes | Write to this ERD to set Smart Assist Cloud Notification. This controls the Smart Assist LED on the dishwasher UI for cloud based notifications. The status for this ERD is stored in 0x310D. |
| Auto Lid Down | 0x320d | 0x320c | switch | Yes | Request whether the drawer lids will open after a cycle has completed or remain closed. |
| Steam Option State | 0x321f | — | binary_sensor | Yes | The current state of the Steam Option State |
| Bottle Blast Option State | 0x3220 | — | binary_sensor | Yes | The current state of the Bottle Blast Option State |
| UltraFresh Option State | 0x3221 | — | binary_sensor | Yes | The current state of the UltraFresh Option State |
| Silverware Wash Option State | 0x322b | — | binary_sensor | Yes | The current state of the Silverware Wash Option State |
| Custom Cycle Index | 0x322c | 0x322d | number | Yes | This is used to request a custom cycle index from a client. uiCycles <= index < totalCycles (these values are defined in ERD 0x3200). If the custom cycle has not been selected, default value is 255. |
| Default to Eco Cycle | 0x3232 | 0x3231 | switch | Yes | Request for whether the product will default to running Eco cycle, or the last selected cycle. |
| Rinse and Hold | 0x3260 | — | binary_sensor | Yes | Requested state of the Rinse and Hold Option |
| Auto Open Door | 0x3263 | — | binary_sensor | Yes | Requested state of the Auto Open Door Option |
| Mixing valve home state | 0x4008 | — | binary_sensor | Yes | Request mixing valve to cycle to full cold |
| Water Heater Boost Mode State | 0x4221 | 0x4220 | switch | Yes | Request the water heater to enable/disable boost mode. |
| Requested Water Valve Position | 0x4223 | — | binary_sensor | Yes | Command to move water valve to given state. |
| Water Heater Active State | 0x4226 | 0x4225 | switch | Yes | Request the water heater to be enabled/disabled. |
| Twelve Hour Shutoff | 0x5000 | — | binary_sensor | Yes | Specifies whether the range will automatically stop cooking if cooking for longer than twelve hours. |
| End Tone | 0x5001 | — | binary_sensor | Yes | The current tone type used to alert either an end of cook or an end of timer to the user. |
| Convection Conversion | 0x5003 | — | binary_sensor | Yes | Specifies whether convection conversion is enabled. |
| Clock Display | 0x5019 | 0x501a | switch | Yes | Request clock display to be enabled/disabled. Acceptance of write can be read in ERD 0x501A. |
| Automatic Door Opener Local Public Enable | 0x502c | — | binary_sensor | Yes | Enables the automatic door opener (voice to open). There is an agreement in place with UL that this enable must set on the unit, so this ERD needs to remain local-only. This ERD is intended as a unit wide request in coordination with cavity statuses in 5118 and 5218. |
| Enhanced Sabbath Cooking Accepted | 0x502f | 0x5030 | switch | Yes | This ERD is used to accept/cancel an Enhanced Sabbath/Holiday cook mode, given the current Enhanced Sabbath State (ERD 0x502E). 1. To to accept the cooking prompt, set this ERD to true while the State is 'Prompt Sabbath' (1) or 'Prompt Holiday' (2). (State will become 'Cooking Accepted, Sabbath Pending' (3) or 'Cooking Accepted, Holiday Pending' (4), respectively.) 2. To revoke acceptance, set this ERD to false while the the State is 'Cooking Accepted, Sabbath Pending' (3) or 'Cooking Accepted, Holiday Pending' (4). (State will revert to 'Prompt Sabbath' (1) or 'Prompt Holiday' (2), respectively.) 3. To cancel an active Sabbath/Holiday cook mode, set this ERD to false while the the State is 'Sabbath Active, Warm' (7), 'Holiday Active, Warm' (8), or 'Holiday Active, Bake' (9). (State will become 'Sabbath Active, No Cooking' (5) or 'Holiday Active, No Cooking' (6), resepctively.) The client is responsible for resetting this ERD to false after the Sabbath/Holiday period ends. See status ERD 0x5030. |
| Enhanced Sabbath Warmness Setting | 0x5031 | 0x5032 | switch | Yes | Request to set the warmness level for Enhanced Sabbath warm cycles. See status ERD 0x5032. |
| Cook Cam AI Assistant Enabled | 0x504e | 0x504f | switch | Yes | Writing to this ERD will request to change the state of the Cook Cam AI Assistant feature. See ERD 0x504F for the Cook Cam AI Assistant Enabled Status. |
| Cook Cam Image Upload Enabled Setting | 0x5053 | 0x5054 | switch | Yes | User setting to enable or disable cook cam image uploads to the cloud. User consent is required. Client should request settings updates via this ERD. |
| Request Upper Door Open | 0x510f | — | binary_sensor | Yes | Writing true to this will attempt to open the upper cavity door. After door open is attempted, control will clear this to false. |
| Upper Oven Do Not Stop Cook Mode On Timer Expiration | 0x511a | 0x511b | number | Yes | Requests whether the cook mode should end when the timer expires in the upper oven. |
| Request Lower Door Open | 0x520f | — | binary_sensor | Yes | Writing true to this will attempt to open the lower cavity door. After door open is attempted, control will clear this to false. |
| Lower Oven Do Not Stop Cook Mode On Timer Expiration | 0x521a | 0x521b | number | Yes | Requests whether the cook mode should end when the timer expires in the lower oven. |
| Start Closed-Loop Cooking Cook Timer | 0x5675 | — | switch | Yes | Start request to run the closed-loop cooking cook timer. |
| Lock Gas Valve | 0x5901 | — | binary_sensor | Yes | Request Gas Valve to be locked. |
| Hood Delay Off | 0x5b04 | — | binary_sensor | Yes | This activates the Delay Off if the unit is On. It can also be used to cancel a pending delay off. |
| Hood Camera Light Assist Level | 0x5b08 | — | binary_sensor | Yes | The current camera light assist setting. When writing, level must be listed as available in available light levels ERD 0x5B09. If 0x5B09 has "Infinite" set, then the Light Level is % with max 100. |
| Hood Request On/Off | 0x5b12 | — | binary_sensor | Yes | This request turns the hood on to product-specific default light/fan settings. When turning the hood off, the product might save the previously used fan/light settings. |
| Hood Delay Off | 0x5b1b | — | binary_sensor | Yes | A request to start or stop the Delay Off Mode |
| Microwave Remote Enable | 0x5c14 | — | binary_sensor | Yes | Microwave Remote Enable. |
| Turntable | 0x5c31 | — | binary_sensor | Yes | The current setting of the turntable.  If MWO supports turntable on/off is defined in 0x5C01. |
| Wireless Connection State | 0x6003 | — | select | Yes | Specifies whether wireless module is connected or not. |
| Voice Feature Enable | 0x630e | — | switch | Yes | This is used to enable the local voice control feature on appliances |
| Zoneline On/Off Control | 0x7001 | — | binary_sensor | Yes | Control the Zoneline unit's state. |
| Energy Conservation | 0x7052 | 0x7054 | select | Yes | A configurable-level of Eco Energy Savings. This applies to any running mode. |
| UVC Kit Enable | 0x73ff | — | binary_sensor | Yes | AUX setting to enable UVC Kit support |
| Smart Fan Cooling | 0x7401 | — | binary_sensor | Yes | AUX setting to control smart fan mode during cooling |
| Smart Fan Heating | 0x7402 | — | binary_sensor | Yes | AUX setting to control smart fan mode during heating |
| Freeze Sentinel | 0x7404 | — | binary_sensor | Yes | AUX setting to allow Freeze Sentinel |
| Heat Sentinel | 0x7405 | — | binary_sensor | Yes | AUX setting to allow Heat Sentinel |
| Constant Fan State | 0x7406 | — | binary_sensor | Yes | AUX setting to control constant fan mode |
| Duct Mode | 0x740a | — | binary_sensor | Yes | AUX setting to configure duct mode |
| Electric Heat Only mode | 0x740b | — | binary_sensor | Yes | AUX setting to control Electric Heat Only mode |
| Boost Heat Mode | 0x740c | — | binary_sensor | Yes | AUX setting to control Boost Heat mode |
| MUAM Occupancy Enabled | 0x740e | — | binary_sensor | Yes | AUX setting to configure MUAM Occupancy Enabled control |
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
| Dehumidifier Pump On/Off State | 0x7830 | — | binary_sensor | Yes | Request to power on/off state for dehumidifier pump. |
| Dehumidifier Nonstop Mode | 0x7833 | 0x7834 | switch | Yes | Request for the dehum to enter nonstop mode. |
| Refrigerant Leak Sensor Error Clear | 0x7858 | — | binary_sensor | Yes | Used to request the leak sensor clear errors. |
| ODU Pan Heater status and control | 0x7911 | — | binary_sensor | Yes | ODU Pan Heater Status and control. |
| Compressor Crankcase Heater status and control | 0x7912 | — | binary_sensor | Yes | Compressor Crankcase Heater Status and control. |
| Defrost status and control | 0x7914 | — | binary_sensor | Yes | Defrost Status and control. |
| Turbo/Quiet Mode Modifier | 0x795e | 0x7963 | select | Yes | Request to set which Mode modifier, Turbo/Quiet, is selected. |
| Self Clean Mode Status and Control | 0x796e | — | binary_sensor | Yes | Self Clean Mode ON/OFF Status and Control. Status must be reset to 0 when Self Clean Mode Terminates |
| External Damper | 0x7974 | 0x7973 | switch | Yes | External Damper ON/OFF Control |
| Vacation Mode (10C Heating Mode) Control | 0x7976 | — | binary_sensor | Yes | A Request to put the Appliance into Vacation Mode. Writing to this ERD can change the mode of the Appliance. |
| Service Mode Electric Room Heater | 0x7977 | — | binary_sensor | Yes | Electric Room Heater ON/OFF Request. This ERD only controls the heater during service mode. |
| Self Clean | 0x7978 | — | binary_sensor | Yes | Client can request self clean actions to occur using this ERD. After client writes the ERD, the value will be immediately written back to `No Request. |
| Temperature Display Mode Selection | 0x7980 | 0x7981 | select | Yes | Overrides the user selected mode for displaying temperature. Temperature can be selected to represent the set-temperature or ambient-temperature. |
| Filter Replacement Interval Reminder | 0x79a0 | 0x79a1 | number | Yes | Request to Change User-Selectable reminder interval, in hours, for a filter change. |
| Local Schedule Enable | 0x79a2 | — | binary_sensor | Yes | Request to Enable Local Scheduling, a schedule stored entirely on the Appliance |
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
| WAC Filter Notification | 0x7a04 | — | binary_sensor | Yes | Notification of whether the filter requires cleaning/replacement |
| WAC Power On/Off State | 0x7a0f | — | binary_sensor | Yes | The power on/off state for WAC products |
| Sleep Mode | 0x7b05 | — | binary_sensor | Yes | Sleep mode for split AC |
| Up-down Air Swing | 0x7b07 | — | binary_sensor | Yes | The vertical (up-down) swing |
| Left-right Air Swing | 0x7b08 | — | binary_sensor | Yes | The horizontal (left-right) swing |
| Eco Mode | 0x7b0c | — | binary_sensor | Yes | Eco mode for Split AC |
| Sleep Mode | 0x7b0e | — | binary_sensor | Yes | Request to turn on/off sleep mode. |
| Water Softener Shutoff Valve Installed | 0x8032 | — | binary_sensor | Yes | Flag indicating whether option is installed |
| Espresso Maker Reset Brew Parameters | 0x9023 | — | button | Yes | Write the ID for the brew parameters to be reset to default |
| Disable Grinder Requested State | 0x9050 | — | binary_sensor | Yes | This ERD is used to disable the grinder in case the user is using pre-ground coffee. Settings: 0 = Enable Grinder 1 = Disable Grinder |
| Ice Maker Cloud Schedule Enabled | 0x9102 | — | binary_sensor | Yes | Whether the cloud schedule is enabled or disabled. |
| Ice Maker Power | 0x9107 | — | binary_sensor | Yes | Power status and control. |
| Ice Maker Filter Status Reset | 0x911d | — | button | Yes | Used to reset the filter status. Write a 1 (true) to reset the filter. |
| Water Level Tone Setting Requested State | 0x9141 | — | switch | Yes | The requested state of the water level tone setting. 0 = off, 1 = on |
| Toaster Oven Cavity Light Requested State | 0x9202 | — | binary_sensor | Yes | The requested state of the cavity light. 0 = off, 1 = on |
| Toaster Oven Door Alarm Silence | 0x9224 | — | binary_sensor | Yes | Silence the door alarm. Write 1 to silence alarm. |
| Toaster Oven Reset Cooking Parameters for the Selected Cooking Mode | 0x9225 | — | button | Yes | Reset the cooking parameters to the factory default for the selected cooking mode. |
| Toaster Oven Cancel Operation | 0x9228 | — | binary_sensor | Yes | Cancel the oven operation.  This command is write-only.  Write a 1 to this ERD to cancel the current oven operation. |
| Toaster Oven Requested Preheat Enabled | 0x922a | — | binary_sensor | Yes | The requested state of the preheat enabled setting. 0 = disabled, 1 = enabled |
| Toaster Oven Requested Convection Fan State | 0x922c | — | binary_sensor | Yes | The requested state of the convection fan. 0 = off, 1 = on Note that not all modes allow the operation of the convection fan. |
| Mixer Pause Mixing Cycle | 0x9304 | — | binary_sensor | Yes | Used to pause the mixing cycle. Write a 1 (true) to pause. |
| Scale Mode Enable | 0x930f | — | binary_sensor | Yes | Used to enable scale feedback by displaying weight measured at the unit UI. Write a 1 (true) to enable the scale.  Mixer will enter scale mode. |
| Tare Scale | 0x9310 | — | binary_sensor | Yes | Used to zero out the scale measurement by taring the scale. Write a 1 (true) to tare the scale. |
| Smoke | 0x9404 | 0x9403 | switch | Yes | The request to enable smoke |
| Smoke Paused | 0x9406 | — | binary_sensor | Yes | The request to pause smoke |
| Auto Warm Enable Requested | 0x9422 | — | binary_sensor | Yes | Auto warm is a feature where if enabled, a warm cycle is initiated once cooking is complete. If auto-warm is disabled the unit transitions to idle once cooking is complete. |
| Early Completion Notification Temperature Threshold | 0x942c | 0x942b | number | Yes | The requested early completion notification temperature threshold setting. The early completion notification based on temperature is triggered when: * Actual probe temperature >= Probe target temperature - Early Completion Notification Temperature Threshold. If the threshold entered by the user is in Celsius then: * ERD Value in (F) = User Entered Value (C) x 9/5  (Rounded to the closest integer). |
| Early Completion Notification Time Threshold | 0x942f | 0x942e | number | Yes | The requested cook time remaining value when the early completion notification is triggered. |
| Reset Cooking Parameters | 0x9434 | — | button | Yes | Resets the cooking parameters to the factory default for the specified mode or modes. |
| Restore Factory Defaults | 0x9435 | — | binary_sensor | Yes | Used to reset all user settings on the unit to factory defaults. Write a true to restore factory defaults. |
| Temperature Offset | 0x9503 | 0x9502 | number | Yes | The requested value of temperature offset setting |
| Temporary Temperature Offset Demand Response | 0xd00b | 0xd00c | number | Yes | Specifies the parameters for a Temperature Offset Demand Response Event |
| Cost of power cost/comfort slider | 0xd00e | 0xd00f | number | Yes | This allows the client to balance cost savings against comfort in the form of stable water temperature A value of 0 will allow full cost savings, which will vary the water heater tank setpoint and charging times in order to maximize use of off-peak power and reduce or eliminate peak priced power. A value of 255 will prioritize temperature setpoint stability at the expense of sometimes using peak priced power. Values between 0 and 255 give a sliding scale of temperature stability vs cost savings |

*Total: 213 controllable ERDs*
