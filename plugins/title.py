from util import hook, http
import urlhistory
import htmlentitydefs
import re
titler = re.compile(r'(?i)<title>(.+?)</title>')

@hook.regex(r".*(minecraftforum\.net/viewtopic\.php\?[\w=&]+)\b.*")
def regex(inp, say=None):
    "titles minecraftforum urls"
    t=title("http://"+inp.group(1)).replace(" - Minecraft Forums","")
    if t=="Login":
        return
    say("mcforum title: "+t)


@hook.command
@hook.command("t")
def title(inp, db=None):
    ".title <url> - get title of <url>"
    if inp == '^':
        urlhistory.db_init(db)
        rows = db.execute("select url from urlhistory order by time desc limit 1")
        if not rows.rowcount:
            return "No url in history."
        inp = rows.fetchone()[0]

    match = titler.search(http.get(inp))
    if not match:
        return "Error: no title"

    rawtitle = match.group(1)

    title = re.sub("&("+"|".join(htmlentitydefs.entitydefs.keys())+");",
                   lambda m: unichr(htmlentitydefs.name2codepoint[m.group(1)]), rawtitle)
    return title
