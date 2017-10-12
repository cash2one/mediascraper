# -*- coding: utf-8 -*-
import re

title_str = "(رامـى صـبرى_وعـد مـنى ♥)sdfرامـى صـبرى_وعـد مـنى 234("
title_str = "(مزمار رأس السنه 2017              sdfعبد السلام 🎤🎹🎶🎶🎧234("
title_str = "GOT7 (갓세븐) “Never Ever” - Piano Cover"

title_str = unicode(title_str, "utf-8")
exactMatch = re.sub(ur"[^\u0000\u0000-\uffff\uffff]", "", title_str, flags=re.UNICODE)
# exactMatch = re.sub(r"(\W+)(^\()", "", unicode(title_str, "utf-8"), flags=re.UNICODE)

# exactMatch = re.findall(ur"[\w]+|\(+|\)+", title_str, flags=re.UNICODE)
# exactMatch = re.findall(ur"[^\u0000\u0000-\uffff\uffff]+", title_str, flags=re.UNICODE)


print "******************"
print title_str
print exactMatch
# print " ".join(exactMatch)

