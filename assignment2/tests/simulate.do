onerror {quit -code 1}
onbreak {quit -code 1}
if {![file exists work]} {vlib work}
vmap work work
vcom -2008 src/and_or4.vhd src/mux8.vhd src/letters7seg.vhd src/voting25.vhd src/popcount13_display.vhd src/hex7seg.vhd tests/tb_assignment2.vhd
vsim work.tb_assignment2
run -all
quit -code 0
