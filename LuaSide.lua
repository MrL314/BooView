















---------------------------------------------------------------------------------------

local socket = require("socket")

--local host, port = "127.0.0.1", 65432
local host, port = "localhost", 65432


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

	--[[
	for str in string.gmatch(s, "([^%s]+)") do
		--console.write(str)
		table.insert(t, str)
	end
	--]]

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


--[[
function is_table_empty(T):
	local next = next
	if next(T) == nil then
		return true
	end
	return false
end
--]]

function onExit()
	close_socket_client("Client Script Forcibly Stopped")
end

event.onexit(onExit)

socket_client = nil


--RECV_BUFFER = {}


--SYNCED = false

function connect_client()

	socket_client = socket.connect(host, port)
	--socket_client:settimeout(0.1, 't')
	--socket_client:settimeout(1, 't')
	socket_client:settimeout(3)
	console.write("\nConnected to " .. socket_client:getpeername())
end

if pcall(connect_client) then
else
	socket_client = nil
end


function socket_client_is_open()
	if socket_client == nil then
		return false
	end
	return true
end


function close_socket_client(msg)
	if socket_client_is_open() then
		console.write("\nDisconnected from " .. socket_client:getpeername() .. ".")
		if msg ~= "" then
			console.write("\nReason: " .. msg .. "\n")
		end
		socket_client:send("close\n" .. msg)
		socket_client:close()
	end
	socket_client = nil
end


function send_data(data)
	if socket_client_is_open() then
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
				console.write("Socket Error: " .. err)
			end
			return err
		end
		
		if data == nil then
			close_socket_client("Server sync failed")
			return nil
		end

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

		if data == "ack" then
			SYNCED = true
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
		socket_client:send("sync\n")
		local data = receive_from_server()

		if data == nil then
			return false
		end

		if data == "ack" then
			--console.write("recieved syn ack")
			return true
		end

		if data == "closed" then
			close_socket_client("Server was forcibly closed.")
			return false
		end

		-- test this to make sure it makes sense
		return true
	end
	return false
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

while true do

	END_TRANSMISSION = false

	while socket_client_is_open() do

		local data = receive_data()


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

			race_checkpoints = memory.readbyte(0x148)

			track_num = memory.readbyte(0x124)

			--local x_pos = memory.read_u16_le(0x1018) * 4
			--local y_pos = memory.read_u16_le(0x101c) * 4
			--local heading = memory.readbyte(0x102b)
			--local camera = memory.readbyte(0x0095)

			local game_type = memory.readbyte(0x2c)

			currentJoypad = joypad.get(player)


			


			-- send data to server
			character_bytes = "CH_DATA"

			-- gamemode
			character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0x36))

			-- ghost enable
			g_enable = memory.readbyte(0x7fff02)
			if g_enable == 0 then
				if memory.readbyte(0x11c1) > 0x84 then
					g_enable = 2
				end
			end
			character_bytes = character_bytes .. string.format("%02x", g_enable)

			-- in demo?
			character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0xe32))

			-- game type
			character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0x2C))

			-- track number
			character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0x124))

			-- camera angle
			character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0x95))
			


			for i=0, 7 do

				-- character number
				character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0x1000 + (i*0x100) + 0x12))

				-- x position
				character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0x1000 + (i*0x100) + 0x18))
				character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0x1000 + (i*0x100) + 0x19))
				-- y position
				character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0x1000 + (i*0x100) + 0x1c))
				character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0x1000 + (i*0x100) + 0x1d))
				-- height
				character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0x1000 + (i*0x100) + 0x1f))
				character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0x1000 + (i*0x100) + 0x20))

				-- heading angle
				character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0x1000 + (i*0x100) + 0x2b))
				
				-- x velocity
				character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0x1000 + (i*0x100) + 0x22))
				character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0x1000 + (i*0x100) + 0x23))
				-- y velocity
				character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0x1000 + (i*0x100) + 0x24))
				character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0x1000 + (i*0x100) + 0x25))


				racer_cp = memory.readbyte(0x1000 + (i*0x100) + 0xc0)
				table_index = 2 * ((racer_cp)%race_checkpoints)
				-- checkpoint x position
				character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0x900 + table_index))
				character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0x901 + table_index))
				-- checkpoint y position
				character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0xa00 + table_index))
				character_bytes = character_bytes .. string.format("%02x", memory.readbyte(0xa01 + table_index))
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
				---obj_bytes = obj_bytes .. string.format("%02x", memory.readbyte(0x1800 + (i*0x40) + 0x12))

				base_address = base_obj_addresses[game_type/2 + 1][i + 1]

				--console.write("\nObject " .. i .. " : " .. string.format("%02x", (base_address / 256) % 256) .. string.format("%02x", (base_address % 256)))

				-- obj address
				obj_bytes = obj_bytes .. string.format("%02x", (base_address % 256))
				obj_bytes = obj_bytes .. string.format("%02x", (base_address / 256) % 256)

				-- x position
				obj_bytes = obj_bytes .. string.format("%02x", memory.readbyte(base_address + 0x18))
				obj_bytes = obj_bytes .. string.format("%02x", memory.readbyte(base_address + 0x19))
				-- y position
				obj_bytes = obj_bytes .. string.format("%02x", memory.readbyte(base_address + 0x1c))
				obj_bytes = obj_bytes .. string.format("%02x", memory.readbyte(base_address + 0x1d))
				-- height
				obj_bytes = obj_bytes .. string.format("%02x", memory.readbyte(base_address + 0x1f))
				obj_bytes = obj_bytes .. string.format("%02x", memory.readbyte(base_address + 0x20))

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
					item_bytes = item_bytes .. string.format("%02x", memory.readbyte(base_address + 0x13))


					-- character number
					ch_num = memory.readbyte(base_address + 0x70)
					item_bytes = item_bytes .. string.format("%02x", memory.readbyte(base_address + 0x70))
					

					user = memory.readbyte(base_address + 0x6b)

					if user == 0 then
						user = 0x10
					end

					--console.write("\naddr " .. string.format("%04x", base_address) .. " val " .. string.format("%02x", ch_num) .. " user " .. string.format("%02x", user) .. "\n")

					user_ch = memory.readbyte(user*256 + 0x12)
					item_bytes = item_bytes .. string.format("%02x", memory.readbyte(user*256 + 0x12))

					-- x position
					item_bytes = item_bytes .. string.format("%02x", memory.readbyte(base_address + 0x18))
					item_bytes = item_bytes .. string.format("%02x", memory.readbyte(base_address + 0x19))
					-- y position
					item_bytes = item_bytes .. string.format("%02x", memory.readbyte(base_address + 0x1c))
					item_bytes = item_bytes .. string.format("%02x", memory.readbyte(base_address + 0x1d))
					-- height
					item_bytes = item_bytes .. string.format("%02x", memory.readbyte(base_address + 0x1f))
					item_bytes = item_bytes .. string.format("%02x", memory.readbyte(base_address + 0x20))

					-- heading angle
					--item_bytes = item_bytes .. string.format("%02x", memory.readbyte(0x1000 + (i*0x100) + 0x2b))
					
					-- x velocity
					--item_bytes = item_bytes .. string.format("%02x", memory.readbyte(0x1000 + (i*0x100) + 0x22))
					--item_bytes = item_bytes .. string.format("%02x", memory.readbyte(0x1000 + (i*0x100) + 0x23))
					-- y velocity
					--item_bytes = item_bytes .. string.format("%02x", memory.readbyte(0x1000 + (i*0x100) + 0x24))
					--item_bytes = item_bytes .. string.format("%02x", memory.readbyte(0x1000 + (i*0x100) + 0x25))
				end

			end


			send_data(character_bytes .. "\n" .. obj_bytes .. "\n" .. item_bytes .. "\n")

			--[[
			if receive_data() ~= "received data" then
				close_socket_client("bad response on item data")
				END_TRANSMISSION = true
				break
			end
			--]]


			emu.frameadvance();
			frame = frame + 1
			



		



			if not sync_with_server() then
				REASON = "BAD SYNC"
				END_TRANSMISSION = true
				break
			end

		elseif string.sub(data, 1, 8) == "DO_GHOST" then

			player = 0x1000
			ghost = 0x1100
			nonce = 0
			
			if memory.readbyte(ghost + 0xc1) < 0x85 then
				for i=0x00,0xff do

					if i == -1 then
						nonce = 0
					
					elseif i == 0x00 or i == 0x01 then
						nonce = 0  -- helps with top screen ghosting
					elseif i == 0x02 or i == 0x03 then
						nonce = 0  -- NEED! means top screen not ghosty

					elseif i == 0x04 or i == 0x05 then
						nonce = 0  -- NEED! means top screen not ghosty

					elseif i == 0x08 or i == 0x08 then
						nonce = 0  -- fixes crash on exit


					elseif i == 0x0a or i == 0x0b then
						nonce = 0  -- NEED! Fixes bottom screen issue

					
						---- onto other data

					
					

					elseif i == 0xd5 then
						local flags = memory.readbyte(ghost + i)

						if flags % 2 == 1 then flags = flags - 1 end

						memory.writebyte(player + i, flags)



					

					
					else
						memory.writebyte(player + i, memory.readbyte(ghost + i))
					end

					
				end

			elseif string.sub(data, 1, 7) == "OVERLAY" then


				overlay_data = ""

				num_tiles = 0

				for i=0,0x3fff do
					local tile = memory.readbyte(0x7f0000 + i)
					if tile >= 0xc0 then
						overlay_data = overlay_data .. string.format("%02x", i % 256)
						overlay_data = overlay_data .. string.format("%02x", (i / 256) % 256)
						overlay_data = overlay_data .. string.format("%02x", tile)
						num_tiles = num_tiles + 1
					end
				end

				overlay_data = string.format("%02x", num_tiles % 256) .. string.format("%02x", (num_tiles / 256) % 256) .. overlay_data

				send_data(overlay_data .. "\n")



			end
			

			--[[
			for i=0x00,0xff do

				if i == -1 then
					nonce = 0
				
				

				

				elseif i == 0x11 or i == 0x12 then
					memory.writebyte(0x1000 + i, memory.readbyte(0x1100 + i))

				elseif i == 0x13 or i == 0x14 or i == 0x15 then
					memory.writebyte(0x1000 + i, memory.readbyte(0x1100 + i))

				
				elseif i >= 0x16 and i <= 0x27 then
					memory.writebyte(0x1000 + i, memory.readbyte(0x1100 + i))
				
				
				elseif i >= 0x98 or i <= 0x9f then
					memory.writebyte(0x1000 + i, memory.readbyte(0x1100 + i))

				--elseif i == 0xc4 or i == 0xc5 then
				--	memory.writebyte(0x1000 + i, memory.readbyte(0x1100 + i))

				
				
				--elseif i == 0xc4 or i == 0xc5 then
				--	memory.writebyte(0x1000 + i, memory.readbyte(0x1100 + i))

				
				
				


				
				
				end

				
			end
			--]]

			memory.writebyte(0x94, memory.readbyte(ghost + 0xa4))
			memory.writebyte(0x95, memory.readbyte(ghost + 0xa5))
			


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
						console.write("W_BYTES Error: no address specified")
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
						console.write("W_BYTES Error: no data specified")
						wasBad = true
						break
					end
				else
					console.write("W_BYTES Error: cannot understand " .. TOK)
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

				memory.writebyte(instr["addr"] + i - 1, instr["data"][i])

			end


			if wasBad == true then
				END_TRANSMISSION = true
				REASON = "wasBad"
			end


		elseif string.sub(data, 1, 7) == "R_BYTES" then

			-- request bytes data



		elseif data == "SOCKET_ERROR_TIMEOUT" then
			--console.write("timeout")
			close_socket_client("Client Timed Out")
			END_TRANSMISSION = true
			break

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
			console.write("\n" .. data)
			break
		end	


		if END_TRANSMISSION == true then
			break
		end


	end


	if END_TRANSMISSION == true then
		break
	end



	frame = frame + 1
	--joypad.set(currentJoypad, player)
	--joypad.set(currentJoypad, player)
	emu.frameadvance();
	--joypad.set(currentJoypad, player)
end


if socket_client ~= nil then
	close_socket_client(REASON)
end
socket_client = nil





