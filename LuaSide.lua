






LUA_VERSION_NUMBER = "2.0"
PY_VERSION_NUMBER = "2.0"







---------------------------------------------------------------------------------------

local socket = require("socket")

--local host, port = "127.0.0.1", 65432
local host, port = "localhost", 65432



emu.yield()










RAM_HIGH_BANK = 0x10000

memory.usememorydomain("WRAM")

--console.write(memory.getcurrentmemorydomain())








ButtonNames = {
	"A",
	"B",
	"X",
	"Y",
	"Up",
	"Down",
	"Left",
	"Right",
	"L"
}


function tokenize(s)
	local t = {}

	local from = 1
	local d_from, d_to = string.find(s, " ", from)
	while d_from do
		table.insert(t, string.sub(s, from, d_from-1))
		from = d_to + 1
		d_from, d_to = string.find(s, " ", from)
	end
	table.insert(t, string.sub(s, from))



	return t
end


function isEndFlag(data)
	if data == nil then
		return true
	elseif data == "close" then
		return true
	end
	return false
end




function onExit()
	close_socket_client("Client Script Forcibly Stopped")
end

event.onexit(onExit)

socket_client = nil

SOCKET_TIMEOUT = 0.01
CURR_TIMEOUT = 0.01
--RECV_BUFFER = {}

CLIENT_NAME = ""
--SYNCED = false

function connect_client()

	socket_client = socket.connect(host, port)
	--socket_client:settimeout(0.1, 't')
	--socket_client:settimeout(1, 't')
	socket_client:settimeout(SOCKET_TIMEOUT)

end



function socket_client_is_open()
	if socket_client == nil then
		return false
	end
	return true
end


function close_socket_client(msg)
	if socket_client_is_open() then
		local ad = socket_client:getpeername()
		if CLIENT_NAME ~= "" then ad = CLIENT_NAME end
		console.write("\n[INFO] Disconnected from " .. ad .. ".")
		if msg ~= "" then
			console.write("\n       Reason: " .. msg .. "\n")
		end
		socket_client:send("close\n" .. msg)
		socket_client:close()
	end
	socket_client = nil
end


function send_data(data)
	if socket_client_is_open() then
		--console.log(">>> " .. data .. "\n")

		socket_client:send(data)
	end
end


function receive_from_server()
	if socket_client_is_open() then
		local data,err = socket_client:receive('*l')

		if err ~= nil then
			if err == "timeout" then
				return "SOCKET_ERROR_TIMEOUT"
			end
			if err ~= "closed" then
				console.write("[ERROR] Socket Error: " .. err .. "\n")
			end
			return err
		end
		
		if data == nil then
			close_socket_client("Server sync failed")
			return nil
		end

		--console.log("<<< " .. data .. "\n")

		return data
	end
	return nil
end


function receive_data()
	if socket_client_is_open() then
		local data = receive_from_server()

		if data == nil then
			close_socket_client("Server sync failed.")
			return nil
		end

		if data == "close" then
			close_socket_client("Server was forcibly closed.")
			return nil
		end

		

		if data == "SOCKET_ERROR_TIMEOUT" then
			return data
		end

		return data

	end
	return nil
end



function sync_with_server()
	if socket_client_is_open() then
		--socket_client:settimeout(nil)
		socket_client:settimeout(0.01)
		send_data("sync\n")

		local FAILURES = 0
		local data = "SOCKET_ERROR_TIMEOUT"

		while data == "SOCKET_ERROR_TIMEOUT" do
			data = receive_from_server()
			FAILURES = FAILURES + 1
			if data == "SOCKET_ERROR_TIMEOUT" then
				emu.frameadvance();
				if FAILURES > 1000 then
					break
				end
			end
		end

		--local data = receive_from_server()
		socket_client:settimeout(SOCKET_TIMEOUT)

		--if data == true then return true

		if data == nil then
			return false
		end

		if data == "ack" then
			--console.write("recieved syn ack")
			return true
		end

		if data == "closed" or data == "close" then
			close_socket_client("Server was forcibly closed.")
			return false
		end

		if data == "SOCKET_ERROR_TIMEOUT" then
			close_socket_client("Server sync failed.")
			return false
		end


		-- test this to make sure it makes sense
		console.write("\n[WARNING] SYNC RECEIVED: " .. data .. "\n")
		return true
	end
	return false
end





function readMemoryBlock(domain, start, block_size)
	local return_domain = memory.getcurrentmemorydomain()

	local block = {}

	memory.usememorydomain(domain)

	local bts = memory.readbyterange(start, block_size)

	for i=0,block_size-1 do
		block[i+1] = string.format("%02x", bts[i])
	end

	memory.usememorydomain(return_domain)

	return table.concat(block)

end


function readMemoryBlock_skipped(domain, start, block_size, skip_freq)

	local return_domain = memory.getcurrentmemorydomain()

	local block = {}

	memory.usememorydomain(domain)

	local bts = memory.readbyterange(start, block_size*skip_freq)

	for i=0,block_size-1 do
		block[i+1] = string.format("%02x", bts[i*skip_freq])
	end


	memory.usememorydomain(return_domain)

	return table.concat(block)

end



function READ_BYTE(addr)

	return memory.readbyte(addr)

end

function WRITE_BYTE(addr, val)

	return memory.writebyte(addr, val)

end

function READ_WORD(addr)

	return READ_BYTE(addr) + 256*READ_BYTE(addr+1)

end

function WRITE_WORD(addr, val)
	WRITE_BYTE(addr, val % 256)
	WRITE_BYTE(addr+1, (val / 256) % 256)
end

local FRAME_COUNT = 2


joypad_buttons = nil
p_joypad = nil

emu.frameadvance();

track_num = 0xff

--readMap()

prev_open = false

local player = 1

local currentJoypad = joypad.get(player)

local frame = 0


local P1_VRAM_A = -1
local P1_VRAM_B = -1
local P1_VRAM_C = -1
local P1_VRAM_D = -1
local P2_VRAM_A = -1
local P2_VRAM_B = -1
local P2_VRAM_C = -1
local P2_VRAM_D = -1

local END_TRANSMISSION = false



local base_item_addresses_gp = {0x1a00, 0x1a80}
local base_item_addresses_mr = {0x1a00, 0x1a80, 0x1b00, 0x1b80, 0x1438, 0x1538, 0x1638, 0x1738}
local base_item_addresses_tt = {}
local base_item_addresses_bt = {0x1a00, 0x1a80, 0x1b00, 0x1b80, 0x1438, 0x1538, 0x1638, 0x1738}

local base_item_addresses = {base_item_addresses_gp, base_item_addresses_mr, base_item_addresses_tt, base_item_addresses_bt}


local base_obj_addresses_gp = {0x1800, 0x1840, 0x1880, 0x18c0, 0x1900, 0x1940, 0x1980, 0x19c0}
local base_obj_addresses_mr = {0x1800, 0x1840, 0x1880, 0x18c0, 0x1900, 0x1940, 0x1980, 0x19c0}
local base_obj_addresses_tt = {0x1800, 0x1840, 0x1880, 0x18c0, 0x1900, 0x1940, 0x1980, 0x19c0}
local base_obj_addresses_bt = {0x1800, 0x1880, 0x1900, 0x1980, 0x1238, 0x1338, 0x1940, 0x19c0}  -- last two are dummy

local base_obj_addresses = {base_obj_addresses_gp, base_obj_addresses_mr, base_obj_addresses_tt, base_obj_addresses_bt}


local REASON = ""

SOCKET_DATA = " "


local prev_map = {}
for i=1,0x4000 do
	table.insert(prev_map, -1)
end

local check_map_updates = false

local paused = false


console.clear()
console.write("=======\n")
console.write("Welcome to BooView's LuaSide (v" .. LUA_VERSION_NUMBER .. ") by MrL314!\n")
console.write("=======")
console.write("\n\n[INFO] Attempting to connect...")
emu.frameadvance()


if pcall(connect_client) then

	END_TRANSMISSION = false

	console.clear()
	console.write("=======\n")
	console.write("Welcome to BooView's LuaSide (v" .. LUA_VERSION_NUMBER .. ") by MrL314!\n")
	console.write("=======")


	local SYNCED = sync_with_server()

	if SYNCED == false then
		close_socket_client("Failed to connect to BooView.")
		END_TRANSMISSION = true
	end




	while socket_client_is_open() do

		
		--local tmt = socket_client:gettimeout()
		socket_client:settimeout(CURR_TIMEOUT)
		local data = receive_data()
		if socket_client_is_open() then socket_client:settimeout(SOCKET_TIMEOUT) end

		

		if isEndFlag(data) then
			END_TRANSMISSION = true
			REASON = "END FLAG"
			break
		end

		

		if string.sub(data, 1, 5) == "FRAME" then
			--sync

			
			

			

			if frame >= 2 then
				frame = 0
			end


			

			race_checkpoints = READ_BYTE(0x148)

			track_num = READ_BYTE(0x124)

			--local x_pos = READ_WORD(0x1018) * 4
			--local y_pos = READ_WORD(0x101c) * 4
			--local heading = READ_BYTE(0x102b)
			--local camera = READ_BYTE(0x0095)

			local game_type = READ_BYTE(0x2c)

			currentJoypad = joypad.get(player)


			


			-- send data to server
			character_bytes = "CH_DATA"

			-- gamemode
			character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x36))

			-- camera mode
			local cm = READ_BYTE(0x2e)
			character_bytes = character_bytes .. string.format("%02x", cm)

			

			-- ghost enable
			g_enable = READ_BYTE(RAM_HIGH_BANK + 0xff02)
			character_bytes = character_bytes .. string.format("%02x", g_enable)

			if g_enable == 0 then
				if cm == 2 then
					if READ_BYTE(0x11c1) > 0x84 then
						g_enable = 2
					end
				elseif cm == 4 then 
					if READ_BYTE(0x10c1) > 0x84 then
						g_enable = 2
					end
				end
			end

			character_bytes = character_bytes .. string.format("%02x", g_enable)


			-- in demo?
			character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0xe32))

			-- game type
			character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x2C))

			-- track number
			character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x124))

			-- track theme
			character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x126))

			-- theme object
			character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0xe30))

			-- camera angle
			character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x95))

			-- camera pos x
			character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x4c))
			character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x4d))

			-- camera pos y
			character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x52))
			character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x53))
			
			

			for i=0, 7 do

				-- character number
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x12))


				-- x coord low
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x16))
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x17))
				-- x coord high
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x18))
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x19))
				-- y coord low
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x1a))
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x1b))
				-- y coord high
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x1c))
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x1d))
				-- z coord low
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x1e))
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x1f))
				-- z coord high
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x20))
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x21))

				-- x velocity
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x22))
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x23))
				-- y velocity
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x24))
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x25))
				-- z velocity
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x26))
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x27))

				-- speed
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0xea))
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0xeb))

				-- max speed
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0xd6))
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0xd7))

				-- acceleration
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0xee))
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0xef))



				-- heading angle
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x2a))
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x2b))

				-- momentum angle
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0xa2))
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0xa3))

				-- camera angle
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0xa4))
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0xa5))

				-- angular velocity
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0xb2))
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0xb3))





				if race_checkpoints ~= 0 then
					racer_cp = READ_BYTE(0x1000 + (i*0x100) + 0xc0)
					table_index = 2 * ((racer_cp)%race_checkpoints)
				else
					table_index = 0
				end


				-- checkpoint x position
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x900 + table_index))
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0x901 + table_index))
				-- checkpoint y position
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0xa00 + table_index))
				character_bytes = character_bytes .. string.format("%02x", READ_BYTE(0xa01 + table_index))
			end



			--send_data(character_bytes .. "\n")

			--[[
			if receive_data() ~= "received data" then
				close_socket_client("No response on ch data")
				END_TRANSMISSION = true
				break
			end
			--]]

			--[[send_data(" ")
			if receive_data() ~= "received data" then
				close_socket_client()
				END_TRANSMISSION = true
				break
			end

			--]]

			obj_bytes = ""
			local base_address = 0

			--obstacles
			for i=0, 7 do

				-- character number
				---obj_bytes = obj_bytes .. string.format("%02x", READ_BYTE(0x1800 + (i*0x40) + 0x12))

				base_address = base_obj_addresses[game_type/2 + 1][i + 1]

				--console.write("\nObject " .. i .. " : " .. string.format("%02x", (base_address / 256) % 256) .. string.format("%02x", (base_address % 256)))

				-- obj address
				obj_bytes = obj_bytes .. string.format("%02x", (base_address % 256))
				obj_bytes = obj_bytes .. string.format("%02x", (base_address / 256) % 256)

				-- x coord low
				obj_bytes = obj_bytes .. string.format("%02x", READ_BYTE(base_address + 0x16))
				obj_bytes = obj_bytes .. string.format("%02x", READ_BYTE(base_address + 0x17))
				-- x coord high
				obj_bytes = obj_bytes .. string.format("%02x", READ_BYTE(base_address + 0x18))
				obj_bytes = obj_bytes .. string.format("%02x", READ_BYTE(base_address + 0x19))
				-- y coord low
				obj_bytes = obj_bytes .. string.format("%02x", READ_BYTE(base_address + 0x1a))
				obj_bytes = obj_bytes .. string.format("%02x", READ_BYTE(base_address + 0x1b))
				-- y coord high
				obj_bytes = obj_bytes .. string.format("%02x", READ_BYTE(base_address + 0x1c))
				obj_bytes = obj_bytes .. string.format("%02x", READ_BYTE(base_address + 0x1d))
				-- z coord low
				obj_bytes = obj_bytes .. string.format("%02x", READ_BYTE(base_address + 0x1e))
				obj_bytes = obj_bytes .. string.format("%02x", READ_BYTE(base_address + 0x1f))
				-- z coord high
				obj_bytes = obj_bytes .. string.format("%02x", READ_BYTE(base_address + 0x20))
				obj_bytes = obj_bytes .. string.format("%02x", READ_BYTE(base_address + 0x21))

			end



			-- items
			local item_bytes = ""
			

			for i=0, 7 do

				if (game_type == 0 and i < 2) or (game_type ~= 0 and game_type ~= 4) then

					base_address = base_item_addresses[game_type/2 + 1][i + 1]

					-- obj address
					item_bytes = item_bytes .. string.format("%02x", (base_address % 256))
					item_bytes = item_bytes .. string.format("%02x", (base_address / 256) % 256)


					-- is alive
					item_bytes = item_bytes .. string.format("%02x", READ_BYTE(base_address + 0x13))


					-- character number
					ch_num = READ_BYTE(base_address + 0x70)
					item_bytes = item_bytes .. string.format("%02x", READ_BYTE(base_address + 0x70))
					

					user = READ_BYTE(base_address + 0x6b)

					if user == 0 then
						user = 0x10
					end

					--console.write("\naddr " .. string.format("%04x", base_address) .. " val " .. string.format("%02x", ch_num) .. " user " .. string.format("%02x", user) .. "\n")

					user_ch = READ_BYTE(user*256 + 0x12)
					item_bytes = item_bytes .. string.format("%02x", READ_BYTE(user*256 + 0x12))

					-- x coord low
					item_bytes = item_bytes .. string.format("%02x", READ_BYTE(base_address + 0x16))
					item_bytes = item_bytes .. string.format("%02x", READ_BYTE(base_address + 0x17))
					-- x coord high
					item_bytes = item_bytes .. string.format("%02x", READ_BYTE(base_address + 0x18))
					item_bytes = item_bytes .. string.format("%02x", READ_BYTE(base_address + 0x19))
					-- y coord low
					item_bytes = item_bytes .. string.format("%02x", READ_BYTE(base_address + 0x1a))
					item_bytes = item_bytes .. string.format("%02x", READ_BYTE(base_address + 0x1b))
					-- y coord high
					item_bytes = item_bytes .. string.format("%02x", READ_BYTE(base_address + 0x1c))
					item_bytes = item_bytes .. string.format("%02x", READ_BYTE(base_address + 0x1d))
					-- z coord low
					item_bytes = item_bytes .. string.format("%02x", READ_BYTE(base_address + 0x1e))
					item_bytes = item_bytes .. string.format("%02x", READ_BYTE(base_address + 0x1f))
					-- z coord high
					item_bytes = item_bytes .. string.format("%02x", READ_BYTE(base_address + 0x20))
					item_bytes = item_bytes .. string.format("%02x", READ_BYTE(base_address + 0x21))

					-- heading angle
					--item_bytes = item_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x2b))
					
					-- x velocity
					--item_bytes = item_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x22))
					--item_bytes = item_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x23))
					-- y velocity
					--item_bytes = item_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x24))
					--item_bytes = item_bytes .. string.format("%02x", READ_BYTE(0x1000 + (i*0x100) + 0x25))
				end

			end




			-- map updating

			map_updates = ""


			if check_map_updates == false then
				--console.write("\nMAP RESET")

				for i=1,0x4000 do
					local tile = READ_BYTE(RAM_HIGH_BANK + i-1)
					prev_map[i] = tile
				end

			else
				

				local SENSING_RADIUS = 5 --3

				for i=1,8 do

					local TILE_IND = 0

					local ch_offs = 0x1000 + (i-1)*0x100

					local tile_ind = READ_WORD(ch_offs + 0x58)


					for xoff= -1 * (SENSING_RADIUS-1), (SENSING_RADIUS-1) do
						for yoff=-1 * (SENSING_RADIUS-1), (SENSING_RADIUS-1) do

							local TILE_IND = (tile_ind + xoff) + (yoff * 128)

							if TILE_IND >= 0 and TILE_IND < 0x4000 then

								local tile = READ_BYTE(RAM_HIGH_BANK + TILE_IND)

								if tile ~= prev_map[TILE_IND + 1] then

									if check_map_updates == true then

										local map_ind = TILE_IND

										map_updates = map_updates .. string.format("%02x", map_ind % 256)
										map_updates = map_updates .. string.format("%02x", (map_ind / 256) % 256)
										map_updates = map_updates .. string.format("%02x", tile)

									end

									prev_map[TILE_IND + 1] = tile
								end

							end

						end
					end

				end

			end

			check_map_updates = true






			local SYNCED = sync_with_server()

			if SYNCED == false then
				REASON = "BAD SYNC"
				END_TRANSMISSION = true
				break
				--emu.frameadvance()
			end




			send_data(character_bytes .. "\n" .. obj_bytes .. "\n" .. item_bytes .. "\n" .. map_updates .. "\n")





			
			


			emu.frameadvance();
			frame = frame + 1
			



		


			

		elseif string.sub(data, 1, 9) == "GHOST_OFF" then

			WRITE_WORD(0x1012, P1_VRAM_A)
			WRITE_WORD(0x1014, P1_VRAM_B)
			WRITE_WORD(0x10B6, P1_VRAM_C)
			WRITE_WORD(0x10B8, P1_VRAM_D)
			WRITE_WORD(0x1112, P2_VRAM_A)
			WRITE_WORD(0x1114, P2_VRAM_B)
			WRITE_WORD(0x11B6, P2_VRAM_C)
			WRITE_WORD(0x11B8, P2_VRAM_D)

			P1_VRAM_A = -1
			P1_VRAM_B = -1
			P1_VRAM_C = -1
			P1_VRAM_D = -1
			P2_VRAM_A = -1
			P2_VRAM_B = -1
			P2_VRAM_C = -1
			P2_VRAM_D = -1



		elseif string.sub(data, 1, 8) == "DO_GHOST" then

			if P1_VRAM_A == -1 then
				P1_VRAM_A = READ_WORD(0x1012)
				P1_VRAM_B = READ_WORD(0x1014)
				P1_VRAM_C = READ_WORD(0x10B6)
				P1_VRAM_D = READ_WORD(0x10B8)
				P2_VRAM_A = READ_WORD(0x1112)
				P2_VRAM_B = READ_WORD(0x1114)
				P2_VRAM_C = READ_WORD(0x11B6)
				P2_VRAM_D = READ_WORD(0x11B8)
			end

			player = 0x1000
			ghost = 0x1100

			disp_mode = READ_BYTE(0x2e)

			if disp_mode == 2 then
				player = 0x1000
				ghost = 0x1100
			elseif disp_mode == 4 then
				player = 0x1100
				ghost = 0x1000
			end

			nonce = 0
			
			if READ_BYTE(ghost + 0xc1) < 0x85 then
				for i=0x00,0xff do

					local no_write = false

					if i == -1 then
						no_write = true

					elseif i >= 0x00 and i <= 0x0f then
						no_write = true
						
					--[[
					elseif i == 0x00 or i == 0x01 then
						nonce = 0  -- helps with top screen ghosting
					elseif i == 0x02 or i == 0x03 then
						nonce = 0  -- NEED! means top screen not ghosty

					elseif i == 0x04 or i == 0x05 then
						nonce = 0  -- NEED! means top screen not ghosty

					elseif i == 0x06 or i == 0x07 then
						nonce = 0  -- NEED! means top screen not ghosty

					elseif i == 0x08 or i == 0x09 then
						nonce = 0  -- fixes crash on exit


					elseif i == 0x0a or i == 0x0b then
						nonce = 0  -- NEED! Fixes bottom screen issue


					elseif i == 0x0c or i == 0x0d then
						nonce = 0  -- NEED! Fixes bottom screen issue

					elseif i == 0x0e or i == 0x0f then
						nonce = 0  -- NEED! Fixes bottom screen issue
					--]]

					--[[
					elseif i >= 0x30 and i < 0x40 then
						nonce = 0  -- is this needed?
					
						---- onto other data
					--]]
					--[[
					elseif i >= 0xb6 and i <= 0xbd then
						nonce = 0  -- NEED? Fixes VRAM stuff?

					elseif i >= 0x70 and i <= 0x7f then
						nonce = 0  -- NEED? Fixes VRAM stuff?
					--]]

					
					
					
					elseif i == 0xd5 then
						local flags = READ_BYTE(ghost + i)

						if flags % 2 == 1 then flags = flags - 1 end

						WRITE_BYTE(player + i, flags)
						no_write = true
					end


					if no_write == false then
						WRITE_BYTE(player + i, READ_BYTE(ghost + i))
					end

					
				end
			end
		

			

			--WRITE_BYTE(0x94, READ_BYTE(ghost + 0xa4))
			--WRITE_BYTE(0x95, READ_BYTE(ghost + 0xa5))


		
		elseif string.sub(data, 1, 7) == "OVERLAY" then


			overlay_data = ""

			num_tiles = 0

			for i=0,0x3fff do
				local tile = READ_BYTE(RAM_HIGH_BANK + i)
				if tile >= 0xc0 then
					overlay_data = overlay_data .. string.format("%02x", i % 256)
					overlay_data = overlay_data .. string.format("%02x", (i / 256) % 256)
					overlay_data = overlay_data .. string.format("%02x", tile)
					num_tiles = num_tiles + 1
				end
			end

			overlay_data = string.format("%02x", num_tiles % 256) .. string.format("%02x", (num_tiles / 256) % 256) .. overlay_data

			send_data(overlay_data .. "\n")

			emu.frameadvance();
			frame = frame + 1




		elseif string.sub(data, 1, 7) == "W_BYTES" then

			-- write bytes instructions

			data = string.sub(data, 9, #data)

			wasBad = false

			local toks = tokenize(data)

			
			local instr = {}

			--console.write(toks)
			local i = 1
			while i <= #toks do

				TOK = toks[i]

				if TOK == "addr" then
					if i+1 <= #toks then
						instr["addr"] = tonumber(toks[i+1])
						i = i + 1
					else
						console.write("[ERROR] W_BYTES Error: no address specified\n")
						wasBad = true
						break
					end
				elseif TOK == "bytes" then
					local W_BYTES = {}
					if i+1 <= #toks then
						while i+1 <= #toks do
							table.insert(W_BYTES, tonumber(toks[i+1]))
							i = i + 1
						end
						instr["data"] = W_BYTES
					else
						console.write("[ERROR] W_BYTES Error: no data specified\n")
						wasBad = true
						break
					end
				else
					console.write("[ERROR] W_BYTES Error: cannot understand " .. TOK .. "\n")
					wasBad = true
				end
				i = i + 1
			end




			if wasBad == true then
				END_TRANSMISSION = true
				break
			end

			--console.write("Writing to " .. instr["addr"] .. "\n")

			for i=1, #instr["data"] do

				WRITE_BYTE(instr["addr"] + i - 1, instr["data"][i])

			end


			if wasBad == true then
				END_TRANSMISSION = true
				REASON = "wasBad"
			end


		elseif string.sub(data, 1, 7) == "R_BYTES" then

			-- request bytes data
			frame = frame



		elseif string.sub(data, 1, 5) == "YIELD" then
			CURR_TIMEOUT = 0.01

			paused = true




		elseif string.sub(data, 1, 7) == "UNYIELD" then
			
			--CURR_TIMEOUT = nil
			CURR_TIMEOUT = 0.01
			paused = false
			client.unpause()


		elseif string.sub(data, 1, 5) == "PAUSE" then
			CURR_TIMEOUT = 0.01

			paused = true
			--client.SetSoundOn(false)
			--emu.frameadvance();
			--client.pause()
			--emu.yield();

			console.write("\n[INFO] Paused\n")
			

			--socket_client:settimeout(0.01)
			--while string.sub(receive_data(), 1, 7) ~= "UNPAUSE" do
			--	frame = frame + 1
			--	emu.frameadvance();
			--end
			--socket_client:settimeout(nil)




		elseif string.sub(data, 1, 7) == "UNPAUSE" then
			
			CURR_TIMEOUT = 0.01
			paused = false
			client.unpause()
			console.write("[INFO] Unpaused\n")




		elseif string.sub(data, 1, 6) == "W_SRAM" then

			data = string.sub(data, 8, #data)


			local toks = tokenize(data)

			

			if not (#toks == 1 and toks[1] == "") then
				memory.usememorydomain("CARTRAM")

				for i=0,#toks-1 do
					WRITE_BYTE(i, tonumber(toks[i+1]))
				end

				memory.usememorydomain("WRAM")
			end







		elseif string.sub(data, 1, 5) == "TRACK" then

			emu.frameadvance();
			frame = frame + 1

			local track_data = ""
			local nonce = ""

			for i=1,8 do
				track_data = readMemoryBlock("WRAM", RAM_HIGH_BANK + ((i-1)*0x800), 0x800)
				send_data(track_data .. "\n")
				nonce = receive_data()

				emu.frameadvance();
				frame = frame + 1
			end
			


		elseif string.sub(data, 1, 4) == "ZONE" then

			emu.frameadvance();
			frame = frame + 1

			local zone_data = ""
			local nonce = ""

			for i=1,2 do
				zone_data = readMemoryBlock("WRAM", RAM_HIGH_BANK + 0x5000 + (i-1)*0x800, 0x800)
				send_data(zone_data .. "\n")
				nonce = receive_data()

				emu.frameadvance();
				frame = frame + 1
			end


		elseif string.sub(data, 1, 4) == "FLOW" then

			emu.frameadvance();
			frame = frame + 1

			local flow_data = ""
			local nonce = ""

			for i=1,2 do
				flow_data = readMemoryBlock("WRAM", RAM_HIGH_BANK + 0x4000 + (i-1)*0x800, 0x800)
				send_data(flow_data .. "\n")
				nonce = receive_data()

				emu.frameadvance();
				frame = frame + 1
			end
			


		elseif string.sub(data, 1, 7) == "PALETTE" then

			emu.frameadvance();
			frame = frame + 1

			local palette_data = readMemoryBlock("WRAM", 0x3a80, 0x200)

			send_data(palette_data .. "\n")
			emu.frameadvance();
			frame = frame + 1


		elseif string.sub(data, 1, 5) == "TILES" then

			emu.frameadvance();
			frame = frame + 1

			local tile_data = ""
			local nonce = ""
			

			for i=1,8 do
				tile_data = readMemoryBlock_skipped("VRAM", ((i-1) * 0x1000) + 1, 0x800, 2)
				send_data(tile_data .. "\n")
				nonce = receive_data()

				emu.frameadvance();
				frame = frame + 1
			end


		elseif string.sub(data, 1, 7) == "CP_DATA" then
			
			emu.frameadvance();
			frame = frame + 1

			local cp_data = readMemoryBlock("WRAM", 0x800, 0x100)
			send_data(cp_data .. "\n")

			emu.frameadvance();
			frame = frame + 1



		elseif string.sub(data, 1, 9) == "RESET_MAP" then

			emu.frameadvance();
			frame = frame + 1

			local return_domain = memory.getcurrentmemorydomain()
			memory.usememorydomain("WRAM")

			local i = 1
			for f=1,8 do
				for k=1,0x800 do
					local tile = READ_BYTE(RAM_HIGH_BANK + i-1)
					prev_map[i] = tile
					i = i + 1
				end
				emu.frameadvance();
				frame = frame + 1
			end

			memory.usememorydomain(return_domain)



			check_map_updates = false

			send_data("nonce\n")





		
		elseif string.sub(data, 1, 10) == "UPDATE_MAP" then
			--[[


			

			local return_domain = memory.getcurrentmemorydomain()
			memory.usememorydomain("WRAM")


			map_updates = ""
			
			local SENSING_RADIUS = 10 --3

			for i=1,8 do

				local TILE_IND = 0

				local ch_offs = 0x1000 + (i-1)*0x100



				local tile_ind = READ_WORD(ch_offs + 0x58)


				for xoff= -1 * (SENSING_RADIUS-1), (SENSING_RADIUS-1) do
					for yoff=-1 * (SENSING_RADIUS-1), (SENSING_RADIUS-1) do

						local TILE_IND = (tile_ind + xoff) + (yoff * 128)

						if TILE_IND >= 0 and TILE_IND < 0x4000 then

							local tile = READ_BYTE(RAM_HIGH_BANK + TILE_IND)

							if tile ~= prev_map[TILE_IND + 1] then

								if check_map_updates == true then

									--console.write(string.format("%04x", TILE_IND) .. " " .. string.format("%02x", prev_map[TILE_IND]) .. " " .. string.format("%02x", tile) .. "\n")

									local map_ind = TILE_IND

									map_updates = map_updates .. string.format("%02x", map_ind % 256)
									map_updates = map_updates .. string.format("%02x", (map_ind / 256) % 256)
									map_updates = map_updates .. string.format("%02x", tile)

								end

								prev_map[TILE_IND + 1] = tile
							end

						end

					end
				end

			end

			check_map_updates = true



			memory.usememorydomain(return_domain)

			send_data(map_updates .. "\n")
			--]]




		elseif string.sub(data, 1, 8) == "ID_BVPY_" then

			local num_id = string.sub(data, 9)


			send_data("ID_BVLUA_" .. LUA_VERSION_NUMBER .. "\n")


			if num_id ~= PY_VERSION_NUMBER then
				-- bad data, close off
				END_TRANSMISSION = true
				REASON = "Cannot identify valid BooView script. Please make sure you are using version " .. LUA_VERSION_NUMBER .. " of BooView."
				break
			else
				CLIENT_NAME = socket_client:getpeername() .. " (" .. data .. ")"
				console.write("\n\n[INFO] ID: ID_BVLUA_" .. LUA_VERSION_NUMBER .. "\n[INFO] Connected to " .. CLIENT_NAME)
			end




		elseif data == "SOCKET_ERROR_TIMEOUT" then
			--console.write("timeout")
			

			--close_socket_client("Client Timed Out")
			--END_TRANSMISSION = true
			--break
			frame = frame -- dummy operation
			-- TODO is this correct???

			if CURR_TIMEOUT ~= nil then
				emu.frameadvance();
				frame = frame + 1
			end


		elseif data == "received data" then

			--
			frame = frame -- dummy operation

		elseif data == "closed" then
			close_socket_client("Server was forcibly closed.")
			END_TRANSMISSION = true

		elseif data == "ack" then


		else
			-- bad data, close off
			END_TRANSMISSION = true
			REASON = "BAD DATA"
			console.write("[ERROR] BAD DATA\n" .. data .. "\n")
			break
		end	


		if END_TRANSMISSION == true then
			break
		end


	end


	if socket_client ~= nil then
		close_socket_client(REASON)
	end
	socket_client = nil



else
	console.write("\n[INFO] Failed to connect to BooView socket. Please make sure to run BooView first!")

	socket_client = nil
end








