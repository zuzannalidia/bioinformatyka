from Bio import Entrez,SeqIO
import pandas as p,matplotlib.pyplot as m
def m_():
 e,k,t=input("Email:"),input("Key:"),input("TaxID:")
 l,H=int(input("Min len:")),int(input("Max len:"))
 Entrez.email,Entrez.api_key=e,k
 x=Entrez.read(Entrez.efetch(db="taxonomy",id=t,retmode="xml"))[0]["ScientificName"]
 print("Organism:",x)
 s=Entrez.read(Entrez.esearch(db="nucleotide",term=f"txid{t}[Organism]",usehistory="y"))
 w,q,c=s["WebEnv"],s["QueryKey"],min(int(s["Count"]),100)
 print("Found:",c)
 r=[a for a in SeqIO.parse(Entrez.efetch(db="nucleotide",rettype="gb",retmode="text",retmax=c,webenv=w,query_key=q),"gb") if l<=len(a.seq)<=H]
 print("Filtered:",len(r))
 d=p.DataFrame([{"Acc":a.id,"Len":len(a.seq),"Desc":a.description}for a in r])
 f=f"taxid_{t}"
 d.to_csv(f+".csv",index=0)
 d = d.sort_values("Len", ascending=False)
 m.plot(d["Acc"],d["Len"],'o-');m.xticks(rotation=90,fontsize=6)
 m.tight_layout();m.savefig(f+".png")
 print("Saved:",f+".csv + .png")
if __name__=="__main__":m_()
