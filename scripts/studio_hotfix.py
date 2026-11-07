#!/usr/bin/env python3
"""Targeted verified fixes from Studio Edition II interactive QA."""
from pathlib import Path
import re
p=Path(__file__).resolve().parent.parent/'index.html'
s=p.read_text('utf8')
assert len(s)>3200000
old=""" if(jump)setTimeout(()=>bellReveal.scrollIntoView({behavior:motion(),block:'start'}),200);
 update();
}"""
new=""" if(jump)setTimeout(()=>bellReveal.scrollIntoView({behavior:motion(),block:'start'}),200);
 // update() is invoked after the progress-state declarations are initialised.
 // Calling it from a restored bell state before that point caused a TDZ error.
}"""
if old in s:
 assert s.count(old)==1
 s=s.replace(old,new,1)
else:
 assert 'Calling it from a restored bell state' in s
assert s.count('id="studio-lightbox-image"')==1
p.write_text(s,encoding='utf8')
print('Return-visit progress TDZ fixed')
