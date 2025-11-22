import streamlit as st
from lark import Tree as LarkTree, Token as LarkToken

import configs
from sources.parser import rockwell_l5x_parser


st.markdown("## Routine parser")
st.markdown(
    "Test parser for discrete routines (multiple lines of rungs) or signle rungs (signle line)."
)

routine_sample = (
    "CPT(OpenTime_HMI[Gen.Aux_var.Shift_Index,0],(OpenTime[Gen.Aux_var.Shift_Index]/(10006060)MOD(24)));\n"
    "XIC(HMI.MB[48])MOV(0,Gen_Counters.Ref.OK_Part)MOV(0,Gen_Counters.Ref.NOK_Part)MOV(0,Gen_Counters.Ref.Total_Part)MOV(0,Gen_Counters.Ref.TRP)MOV(0,Gen_Counters.Ref.PPM);"
)
routine_plain = st.text_area("Routine", height=400, placeholder=routine_sample)

if routine_plain:
    parsed_routine: LarkTree = rockwell_l5x_parser.parse(routine_plain)
    st.code(parsed_routine.pretty())
