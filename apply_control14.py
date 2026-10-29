#!/usr/bin/env python3
"""CONTROL1.4 hash-checked changed-only installer. Python3.10+ stdlib; no save deletion."""
from pathlib import Path
import argparse,json,hashlib,shutil,time,re,base64,tempfile,os
HOME=Path(__file__).resolve().parent
def require(ok,message):
 if not ok:raise ValueError(message)
def sha(p):
 h=hashlib.sha256()
 with p.open('rb')as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b)
 return h.hexdigest()
def safe(root,rel):
 require(not Path(rel).is_absolute()and'..'not in Path(rel).parts,'Unsafe path:'+rel)
 candidate=root/rel
 require(not any(q.is_symlink()for q in [candidate,*[root/x for x in Path(rel).parents]]),'Refuse source symlink: '+rel)
 p=candidate.resolve();require(p.is_relative_to(root.resolve()),'Path escapes root:'+rel);return p
def atomic(p,writer):
 fd,name=tempfile.mkstemp(prefix='.control14-',dir=p.parent);os.close(fd);tmp=Path(name)
 try:writer(tmp);os.replace(tmp,p)
 finally:tmp.unlink(missing_ok=True)
def copy(src,p):atomic(p,lambda t:shutil.copy2(src,t))
def ready(path):
 d=json.loads((HOME/'READY_131_TO_14_DELTA.json').read_text());path=path.resolve();require(sha(path)==d['beforeSHA256'],'Expected exact ready CONTROL1.3.1, not1.1 or a transported/edited HTML. Source install remains available.')
 old=path.read_text(encoding='utf-8');m=re.search(r'<script id="foundation-assets" type="application/json">(.*?)</script>',old,re.S);require(m,'Asset block not found');assets=json.loads(m.group(1))
 for r in d['resources']:
  p=safe(HOME/'payload',r['path']);assets[r['key']]=r['prefix']+base64.b64encode(p.read_bytes()).decode()
 def build(part,ops):return ''.join(part[a['copy'][0]:sum(a['copy'])]if'copy'in a else a['insert']for a in ops)
 new=build(old[:m.start(1)],d['pre'])+json.dumps({k:assets[k]for k in d['order']},ensure_ascii=False,separators=(',',':'))+build(old[m.end(1):],d['post']);require(hashlib.sha256(new.encode()).hexdigest()==d['afterSHA256'],'Generated standalone mismatch')
 out=path.with_name('IRON_DUNGEON_CONTROL_14_PLAY.html');require(not out.exists()or sha(out)==d['afterSHA256'],'Output exists with other contents; preserve it first')
 if not out.exists():atomic(out,lambda t:t.write_text(new,encoding='utf-8',newline=''))
 print('READY:',out,'SHA256',sha(out),'Original preserved:',path,'\nOpen NEW PLAY14, not old START.html.')
def install(root,dry):
 mf=json.loads((HOME/'PATCH_MANIFEST_14.json').read_text());todo=[]
 for f in mf.get('protected',[]):
  p=safe(root,f['path']);require(p.is_file()and sha(p)==f['sha256'],'Protected base mismatch: '+f['path'])
 for f in mf['files']:
  p=safe(root,f['path']);src=safe(HOME/'payload',f['path']);require(sha(src)==f['sha256'],'Payload mismatch:'+f['path'])
  if p.exists()and sha(p)==f['sha256']:continue
  require(not p.exists()if f['action']=='ADD'else p.is_file()and sha(p)in[f['beforeSHA256'],*f.get('compatibleBeforeSHA256',[])],'Local changes/base mismatch; no files written: '+f['path']);todo.append((f,p,src))
 print('Validated',len(todo),'changes; DELETE0')
 if dry or not todo:return
 backup=root/('.control14-backup-'+time.strftime('%Y%m%d-%H%M%S')+'-'+str(time.time_ns()));backup.mkdir(exist_ok=False);journal=[]
 for f,p,src in todo:
  if p.exists():b=safe(backup,f['path']);b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,b)
  item=dict(f)
  if p.exists():item['beforeSHA256']=sha(p)
  journal.append(item)
 (backup/'journal.json').write_text(json.dumps(journal,indent=2))
 applied=[]
 try:
  for f,p,src in todo:p.parent.mkdir(parents=True,exist_ok=True);copy(src,p);applied.append((f,p))
 except Exception:
  for f,p in reversed(applied):
   if f['action']=='ADD':p.unlink(missing_ok=True)
   else:copy(safe(backup,f['path']),p)
  raise
 print('Source installed. Backup:',backup,'\nRebuild: cd foundation && npm ci && npm run build:single. Old standalone was NOT changed.')
def rollback(root,backup):
 rows=json.loads((backup/'journal.json').read_text())
 for f in rows:
  p=safe(root,f['path']);require(p.is_file()and sha(p)==f['sha256'],'Post-install local edit: stop without overwriting '+f['path'])
  if f['action']=='REPLACE':require(sha(safe(backup,f['path']))==f['beforeSHA256'],'Backup corrupt')
 for f in reversed(rows):
  p=safe(root,f['path'])
  if f['action']=='ADD':p.unlink() # Exact added file only; never delete directories.
  else:copy(safe(backup,f['path']),p)
 print('Rollback complete; source restored, saves untouched. Rebuild old standalone if required.')
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--root',type=Path);a.add_argument('--dry-run',action='store_true');a.add_argument('--ready',type=Path);a.add_argument('--rollback',type=Path);args=a.parse_args()
 if args.ready:ready(args.ready)
 else:
  require(args.root,'Provide --root DIRECTORY containing foundation/, or --ready existing1.3.1.html')
  if args.rollback:rollback(args.root.resolve(),args.rollback.resolve())
  else:install(args.root.resolve(),args.dry_run)
