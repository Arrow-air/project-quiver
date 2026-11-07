-- relay_delayed_close.lua
-- Quiver SSR auto-engage. Closes relay 1 (main power SSR) 12 seconds after
-- boot so the pre-charge settles before the ESCs see pack voltage.
-- Pilot Handbook 2.4 and 3.4, Initial Configuration Guide 11.3 to 11.5.
--
-- Requires, on the flight controller:
--   SCR_ENABLE      = 1        (Lua scripting enabled, set only after this
--                               file is on the SD card)
--   RELAY1_FUNCTION = 1        (relay output enabled, set first and reboot)
--   RELAY1_PIN      = 105      (IO_CH5 on the Dev-Kit Main PCB)
--   RELAY1_DEFAULT  = 0        (SSR starts open; this script closes it)
-- Place this file in APM/scripts/ on the FC SD card.
--
-- The script does not read the kill switch (RC8_OPTION 28). The relay
-- closes at 12 s whatever the switch position, and the switch acts only
-- when it moves afterwards. Set ch8 to RUN before powering the aircraft
-- (Pilot Handbook 3.2 step 5).

local RELAY_NUM = 0        -- relay index (0-based: relay 1 = index 0)
local DELAY_MS = 12000     -- delay after boot in milliseconds
local armed = false

function update()
    if not armed and millis() > DELAY_MS then
        relay:on(RELAY_NUM)
        armed = true
        gcs:send_text(6, "Relay 1 closed (SSR enabled) after 12s delay")
    end
    return update, 1000
end

return update, 1000
