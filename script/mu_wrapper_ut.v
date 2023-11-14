////////////////////////////////////////////////
//author 	: 	wangxx
//verision	:	V1.00
//last time	:	2022-02-08
//function	:	the top of rce's mu module
///////////////////////////////////////////////


module mu_wrapper_ut
#(
	parameter MEMCONFIG_WIDTH =32
)
(
	//global
	//novif start
	input hclk							,
	input hrst_n						,
	input clk							,
	input rst_n							,
	input test_mode						,
	input [MEMCONFIG_WIDTH-1:0]		memconfig,

	//interrupt //ahb clk
	output interrupt					,
	//novif end

	//rce ahb-lite no burst //ahb clk
	//verify start ahb#master#0
	output			hready_resp			,
	output	[31:0]	hrdata				,
	output	[ 1:0]	hresp				,
	input			hsel,
	input	[31:0]	haddr,
	input			hready,
	input 	[ 1:0]	htrans,
	input 	[ 2:0]	hsize,
	input 	[ 2:0]	hburst,
	input			hwrite,
	input	[31:0]	hwdata,
	//verify end ahb#master#0

	/////////////////////////////////////////////
	//MU interface
	/////////////////////////////////////////////

	//CU inf
	//verify start cu
	input				cu_reg,
	input 				cu_we,
	input	 [3:0]		cu_be,
	input	[32-1:0]	cu_addr,
	input	[32-1:0]	cu_wdata,
	output				cu_valid,
	output 	[32-1:0]	cu_rdata,
	//verify end cu


	//WDMA inf
	//verify start dma
	output				dma_wr_req,
	output	[32-1:0]	dma_wr_reg_addr,
	output	[32-1:0]	dma_wr_reg_len,
	output	[32-1:0]	dma_wr_reg_num,
	output	[32-1:0]	dma_wr_reg_inc,
	output	[32-1:0]	dma_wr_resp_addr,
	input				dma_wr_idle,
	//RDMA inf
	output				dma_rd_req,
	output	[32-1:0]	dma_rd_reg_addr,
	output	[32-1:0]	dma_rd_reg_len,
	output	[32-1:0]	dma_rd_reg_num,
	output	[32-1:0]	dma_rd_reg_inc,
	output	[32-1:0]	dma_rd_resp_addr,
	input				dma_rd_idle,
	//B2B inf
	output				b2b_req,
	output				b2b_conflict,
	output	 [4-1:0]	b2b_opcode,
	output	[32-1:0]	b2b_srcaddr,
	output	[32-1:0]	b2b_dstaddr,
	output	[32-1:0]	b2b_pattern,
	output	[12-1:0]	b2b_dtype,
	output	[20-1:0]	b2b_w,
	output	[20-1:0]	b2b_h,
	input				b2b_idle,
	//verify end dma


	//CSPM inf
	//verify start cspm
	input				dma_w,
	input	[16-1:0]	dma_w_byte,
	input	[32-1:0]	dma_w_addr,
	input  [128-1:0]	dma_w_data,
	//verify end cspm


	//PEA ctrl inf
	//verify start pea
	output				pea_start,
	output	 [4-1:0]	pea_cluster_en,
	input				pea_lsu_idle,
	//pea&lsu CFG inf
	output	 			pea_lsu_cfg_en,
	output	 [6-1:0]	pea_lsu_cfg_addr,
	output[1280-1:0]	pea_lsu_cfg_data,
	//pea PRAM inf
	output	 			pea_parm_clear,
	output	 			pea_parm_en_0,
	output	[10-1:0]	pea_parm_addr_0,
	output	[32-1:0]	pea_parm_data_0,
	output	 			pea_parm_en_1,
	output	[10-1:0]	pea_parm_addr_1,
	output	[32-1:0]	pea_parm_data_1,
	output	 			pea_parm_en_2,
	output	[10-1:0]	pea_parm_addr_2,
	output	[32-1:0]	pea_parm_data_2,
	output	 			pea_parm_en_3,
	output	[10-1:0]	pea_parm_addr_3,
	output	[32-1:0]	pea_parm_data_3,
	//verify end pea


	//LSU inf
	//verify start lsu
	output				lsu_last_en,
	output				lsu_last_use,
	output	 [5-1:0]	lsu_last_chan,
	output	[24-1:0]	lsu_last_num,
	//verify end lsu


	/////////////////////////////////////////////
	//ahbcfg interface
	/////////////////////////////////////////////

	//soft clear
	//novif start
	output				cfg_mu_clear,
	output				cfg_pea_clear,
	output				cfg_lsu_clear,
	//novif end


	//apb interface to icache
	//verify start icache
	output	[32-1:0]	icache_paddr,
	output				icache_penable,
	output				icache_psel,
	output				icache_pwrite,
	output	[32-1:0]	icache_pwdata,
	input				icache_pready,
	input	[32-1:0]	icache_prdata,
	input				icache_pslverr,
	//verify end icache


	//sram interface to cu
	//verify start sram2cu
	output				cfg_cu_vld,
	output				cfg_cu_we,
	output	[32-1:0]	cfg_cu_addr,
	output	[32-1:0]	cfg_cu_wdata,
	output	 [4-1:0]	cfg_cu_be,
	input	[32-1:0]	cfg_cu_rdata,
	//verify end sram2cu


	//sram interface to isp
	//verify start sram2isp
	output				cfg_isp_vld,
	output				cfg_isp_we,
	output	[32-1:0]	cfg_isp_addr,
	output	[32-1:0]	cfg_isp_wdata,
	output	 [4-1:0]	cfg_isp_be,
	input	[32-1:0]	cfg_isp_rdata,
	//verify end sram2isp


	//sram interface to btrom
	//verify start sram2btrom
	output				cfg_btrom_vld,
	output				cfg_btrom_we,
	output	[32-1:0]	cfg_btrom_addr,
	output	[32-1:0]	cfg_btrom_wdata,
	output	 [4-1:0]	cfg_btrom_be,
	input	[32-1:0]	cfg_btrom_rdata,
	//verify end sram2btrom


	//sram interface to dtcm
	//verify start sram2dtcm
	output				cfg_dtcm_vld,
	output				cfg_dtcm_we,
	output	[32-1:0]	cfg_dtcm_addr,
	output	[32-1:0]	cfg_dtcm_wdata,
	output	 [4-1:0]	cfg_dtcm_be,
	input	[32-1:0]	cfg_dtcm_rdata,
	//verify end sram2dtcm


	//sram interface to dspm
	//verify start sram2dspm
	output				cfg_dspm_vld,
	output				cfg_dspm_we,
	output	[32-1:0]	cfg_dspm_addr,
	output	[32-1:0]	cfg_dspm_wdata,
	output	 [4-1:0]	cfg_dspm_be,
	input	[32-1:0]	cfg_dspm_rdata,
	//verify end sram2dspm


	//novif start
	output				intr2cu,
	input	 [4-1:0]	cu_exception,
	input	 [4-1:0]	pea_exception,
	input	 [4-1:0]	lsu_exception,
	input	 [4-1:0]	dma_exception,
	//novif end

    //cucmd inf
	//verify start cucmd
	input 				cu_cmd_req,
	output 				cu_cmd_gnt,
	input 				cu_cmd_we,
	input	 [4-1:0]	cu_cmd_be,
	input	[32-1:0]	cu_cmd_addr,
	input	[32-1:0]	cu_cmd_wdata,
	output	 			cu_rsp_valid,
	output	[32-1:0]	cu_rsp_rdata,
	//verify end cucmd


);


endmodule : mu_wrapper_ut