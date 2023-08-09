#!/usr/bin/python
#
# rotate STS-2 data from UVW to ZNE (or vice-versa)
#
# by AndBro @2022
# __________________________


def __rotate_STS2(st, mode="ZNE->UVW"):
    '''

    PARAMETERS:
        - st        obspy stream 
        - mode      either "ZNE->UVW" or "UVW->ZNE"

    '''    


    from numpy import sqrt

    st_out= st.copy()

    if mode == "ZNE->UVW":
        Z = st.select(channel="*Z")[0].data
        N = st.select(channel="*N")[0].data
        E = st.select(channel="*E")[0].data
        
        st_out[0].data = - sqrt(2/3) * E                 + sqrt(1/3) * Z
        st_out[1].data =   sqrt(1/6) * E + sqrt(1/2) * N + sqrt(1/3) * Z
        st_out[2].data =   sqrt(1/6) * E - sqrt(1/2) * N + sqrt(1/3) * Z

        st_out[0].stats.channel = st[0].stats.channel[:-1] +"U"
        st_out[1].stats.channel = st[1].stats.channel[:-1] +"V"
        st_out[2].stats.channel = st[2].stats.channel[:-1] +"W"
    
    elif mode == "UVW->ZNE":
        
        U = st.select(channel="*U")[0].data
        V = st.select(channel="*V")[0].data
        W = st.select(channel="*W")[0].data
        
        st_out[0].data = - sqrt(2/3) * U + sqrt(1/6) * V + sqrt(1/6) * W
        st_out[1].data =                   sqrt(1/2) * V - sqrt(1/2) * W
        st_out[2].data =   sqrt(1/3) * U + sqrt(1/3) * V + sqrt(1/3) * W

        st_out[0].stats.channel = st[0].stats.channel[:-1] +"E"
        st_out[1].stats.channel = st[1].stats.channel[:-1] +"N"
        st_out[2].stats.channel = st[2].stats.channel[:-1] +"Z"
            
    
    return st_out

## End of File
