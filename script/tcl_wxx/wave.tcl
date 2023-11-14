
proc fsdb_dump{}
{
    fsdbDumpile "sim.fsdb"
    fsdbDumpvars 0 tb_top
    fsdbDumpMDA 0 tb_top
    fsdbDumpon
}

if {env(MY_FSDB_DUMP) == "on"}
{
    fsdb_dump
}
run