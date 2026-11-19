import hashlib,os,sys,shutil
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
from quest_data import CATS
from tips_data import TIPS
ROOT=os.path.join(os.environ["APPDATA"],"PrismLauncher","instances","MP 1.21.1","minecraft","config","ftbquests","quests")
def hid(*a): return hashlib.md5("|".join(a).encode()).hexdigest()[:16].upper()
def q(s): return '"'+s.replace("\\","\\\\").replace('"','\\"')+'"'
def pretty(item):
    n=item.split(":")[1].replace("_"," ").title(); return n
GROUPS=[("mods","Mods"),("tips","Tips")]
gid={k:hid("group",k) for k,_ in GROUPS}
chapters=[]  # (file,title,icon,group,quests=[(id,x,y,item,title,subtitle,descs)])
COLS=6; STEP=1.5
for f,title,icon,mods in CATS:
    qs=[]
    for i,(name,item,desc) in enumerate(mods):
        qid=hid("quest",f,name)
        if item: d2="Craft or obtain %s to complete this quest."%pretty(item)
        else: d2="This mod works in the background or has no single item. Click to complete once you have read this."
        qs.append((qid,(i%COLS)*STEP,(i//COLS)*STEP,item,"&b"+name+"&r",title,[desc,d2]))
    chapters.append((f,title,icon,"mods",qs))
for f,title,icon,tips in TIPS:
    qs=[]
    for i,(name,item,text) in enumerate(tips):
        qid=hid("tip",f,name)
        qs.append((qid,(i%COLS)*STEP,(i//COLS)*STEP,"" ,"&e"+name+"&r","Tip",[text,"Click to mark this tip as read."],item))
    chapters.append((f,title,icon,"tips",qs))
for sub in ("chapters","lang/en_us/chapters"): os.makedirs(os.path.join(ROOT,sub),exist_ok=True)
open(os.path.join(ROOT,"data.snbt"),"w",encoding="utf-8",newline="\n").write('''{
	default_autoclaim_rewards: "disabled"
	default_consume_items: false
	default_quest_disable_jei: false
	default_quest_shape: "square"
	default_reward_team: false
	detection_delay: 60
	disable_gui: false
	drop_loot_crates: false
	emergency_items_cooldown: 300
	grid_scale: 0.5d
	icon: {
		id: "ftbquests:book"
	}
	lock_message: ""
	loot_crate_no_drop: {
		boss: 0
		monster: 600
		passive: 4000
	}
	pause_game: false
	progression_mode: "flexible"
	show_lock_icons: true
	version: 13
}
''')
open(os.path.join(ROOT,"chapter_groups.snbt"),"w",encoding="utf-8",newline="\n").write("{\n\tchapter_groups: [\n"+"".join('\t\t{\n\t\t\tid: "%s"\n\t\t\ttitle: %s\n\t\t}\n'%(gid[k],q(tt)) for k,tt in GROUPS)+"\t]\n}\n")
lang_chapter=[];lang_group=["\tchapter_group.%s.title: %s"%(gid[k],q(t)) for k,t in GROUPS]
for order,(f,title,icon,grp,qs) in enumerate(chapters):
    cid=hid("chapter",f)
    out=["{","\tdefault_hide_dependency_lines: false",'\tdefault_quest_shape: "square"','\tfilename: %s'%q(f),'\tgroup: "%s"'%gid[grp],"\ticon: {",'\t\tid: %s'%q(icon),"\t}",'\tid: "%s"'%cid,'\ttitle: %s'%q(title),"\timages: [ ]","\torder_index: %d"%order,"\tquest_links: [ ]","\tquests: ["]
    lang=[]
    for qq in qs:
        qid,x,y,item=qq[0],qq[1],qq[2],qq[3]; qtitle,sub,descs=qq[4],qq[5],qq[6]; ticon=qq[7] if len(qq)>7 else item
        out.append("\t\t{")
        if ticon: out+=["\t\t\ticon: {",'\t\t\t\tid: %s'%q(ticon),"\t\t\t}"]
        out.append('\t\t\tid: "%s"'%qid)
        out.append("\t\t\tsubtitle: %s"%q(sub))
        out.append("\t\t\ttitle: %s"%q(qtitle))
        out.append("\t\t\tdescription: [%s]"%", ".join(q(d) for d in descs))
        out.append("\t\t\ttasks: [{")
        out.append('\t\t\t\tid: "%s"'%hid("task",qid))
        if item: out+=['\t\t\t\titem: { count: 1, id: %s }'%q(item),'\t\t\t\ttype: "item"']
        else: out.append('\t\t\t\ttype: "checkmark"')
        out.append("\t\t\t}]")
        out+=["\t\t\tx: %.1fd"%x,"\t\t\ty: %.1fd"%y,"\t\t}"]
        lang.append("\tquest.%s.quest_desc: [%s]"%(qid,", ".join(q(d) for d in descs)))
        lang.append("\tquest.%s.quest_subtitle: %s"%(qid,q(sub)))
        lang.append("\tquest.%s.title: %s"%(qid,q(qtitle)))
    out+=["\t]","}"]
    open(os.path.join(ROOT,"chapters",f+".snbt"),"w",encoding="utf-8",newline="\n").write("\n".join(out)+"\n")
    open(os.path.join(ROOT,"lang/en_us/chapters",f+".snbt"),"w",encoding="utf-8",newline="\n").write("{\n"+"\n".join(sorted(lang))+"\n}\n")
    lang_chapter.append("\tchapter.%s.title: %s"%(cid,q(title)))
open(os.path.join(ROOT,"lang/en_us/chapter.snbt"),"w",encoding="utf-8",newline="\n").write("{\n"+"\n".join(lang_chapter)+"\n}\n")
open(os.path.join(ROOT,"lang/en_us/chapter_group.snbt"),"w",encoding="utf-8",newline="\n").write("{\n"+"\n".join(lang_group)+"\n}\n")
print("chapters:",len(chapters),"quests:",sum(len(c[4]) for c in chapters),"->",ROOT)
# titles and text are written inline in the chapter files, so drop the lang folder
shutil.rmtree(os.path.join(ROOT,"lang"),ignore_errors=True)
