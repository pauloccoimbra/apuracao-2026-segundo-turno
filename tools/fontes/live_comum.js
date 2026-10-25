const {ALLU,UFN,D,D26,U1,U1vv,IL,IF,pctSec,fin,startLive,codesCard,bindCodes}=AP;
const $=(s,r=document)=>r.querySelector(s),esc=AP.esc,fi=AP.fi,fd=AP.fd,fp=AP.fp,fs=AP.fs;
function wire(need){$('#codesbox').innerHTML=codesCard();bindCodes();startLive(need)}
