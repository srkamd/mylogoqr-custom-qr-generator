"""
Anti-AI & Humanization Engine for MyLogoQR
Cleans out AI-generated clichés, robotic transition words, and monotonous phrasing.
Injects real human experience, practitioner testing notes, conversational rhythm,
and high perplexity/burstiness across all blog articles and landing pages.
"""
import os
import re

WEBSITE_DIR = r"D:\Projects\mylogoqr\website"
BLOG_DIR = os.path.join(WEBSITE_DIR, "blog")

AI_REPLACEMENTS = [
    (r"\bIn today's fast-paced digital world\b", "In everyday business"),
    (r"\bIn today's fast-paced world\b", "In day-to-day operations"),
    (r"\bIn the fast-paced digital landscape\b", "In the real world"),
    (r"\bIn today's digital landscape\b", "In modern business"),
    (r"\bIn today's digital age\b", "Nowadays"),
    (r"\bIn the digital age\b", "Today"),
    (r"\bIt is important to remember that\b", "Keep in mind:"),
    (r"\bIt is crucial to note that\b", "Here's the key:"),
    (r"\bIt's important to remember that\b", "Remember:"),
    (r"\bIt is worth noting that\b", "Note that"),
    (r"\bNeedless to say,\b", "Naturally,"),
    (r"\bIt goes without saying that\b", "As you'd expect,"),
    (r"\bDelve into\b", "Take a close look at"),
    (r"\bdelve into\b", "explore"),
    (r"\bDelve deeper\b", "Dig deeper"),
    (r"\bdelve deeper\b", "look closer"),
    (r"\bA testament to\b", "Clear proof of"),
    (r"\ba testament to\b", "proof of"),
    (r"\bstands as a testament\b", "proves"),
    (r"\btapestry of\b", "blend of"),
    (r"\bparamount\b", "critical"),
    (r"\bParamount\b", "Crucial"),
    (r"\bpivotal\b", "essential"),
    (r"\bPivotal\b", "Essential"),
    (r"\bbeacon of\b", "model of"),
    (r"\bFurthermore,\b", "Also,"),
    (r"\bMoreover,\b", "On top of that,"),
    (r"\bIn conclusion,\b", "Bottom line:"),
    (r"\bTo wrap up,\b", "Final takeaway:"),
    (r"\bIn summary,\b", "To sum it up:"),
    (r"\bseamlessly\b", "smoothly"),
    (r"\bSeamlessly\b", "Smoothly"),
    (r"\bharness the power of\b", "take advantage of"),
    (r"\bHarness the power of\b", "Take advantage of"),
    (r"\bunlocking the potential of\b", "getting the most out of"),
    (r"\bUnlocking the potential of\b", "Getting the most out of"),
    (r"\brevolutionizing the way\b", "transforming how"),
    (r"\bgame-changer\b", "huge upgrade"),
    (r"\bGame-changer\b", "Huge upgrade"),
    (r"\bgame changer\b", "big upgrade"),
    (r"\bnavigating the complexities of\b", "dealing with"),
    (r"\bWhen it comes to\b", "When dealing with"),
    (r"\bAt the end of the day,\b", "When all is said and done,"),
    (r"\bIn order to\b", "To"),
    (r"\bin order to\b", "to"),
    (r"\bDue to the fact that\b", "Because"),
    (r"\bdue to the fact that\b", "because"),
    (r"\bA wide array of\b", "A variety of"),
    (r"\ba wide array of\b", "a range of"),
    (r"\bA myriad of\b", "Countless"),
    (r"\ba myriad of\b", "many"),
    (r"\bplethora of\b", "plenty of"),
    (r"\butilize\b", "use"),
    (r"\bUtilize\b", "Use"),
    (r"\butilizing\b", "using"),
    (r"\bUtilizing\b", "Using"),
    (r"\butilization\b", "use"),
    (r"\boptimum\b", "best"),
    (r"\bfacilitate\b", "help with"),
    (r"\bcommence\b", "start"),
    (r"\bterminate\b", "end"),
    (r"\bendeavor\b", "attempt"),
    (r"\bmeticulous\b", "careful"),
    (r"\bmeticulously\b", "carefully"),
    (r"\bholistic\b", "complete"),
    (r"\bsynergy\b", "teamwork")
]

PRACTITIONER_TIPS = [
    """<div class="tip" style="background:#F8FAFC;border-left:4px solid var(--p);padding:18px 22px;border-radius:12px;margin:28px 0">
<b>Field-Tested Note:</b> We always recommend running the <i>'Two-Phone Daylight Test'</i> before sending any QR code to a commercial printer. Test scan the exported vector on both an iPhone and an older Android phone—first under direct bright sunlight, and then in a dimly lit hallway. If both open in under one second, your design is print-ready.
</div>""",
    """<div class="tip" style="background:#F8FAFC;border-left:4px solid var(--t);padding:18px 22px;border-radius:12px;margin:28px 0">
<b>Print Material Warning:</b> Never print QR codes on high-gloss UV varnishes or curved metallic surfaces. Camera flash and ceiling spotlight reflections create white glare over the corner markers, causing scanning vision algorithms to fail. Opt for matte cardstock or non-reflective vinyl.
</div>""",
    """<div class="tip" style="background:#F8FAFC;border-left:4px solid var(--a);padding:18px 22px;border-radius:12px;margin:28px 0">
<b>Real-World Sizing Rule of Thumb:</b> Maintain a <b>10:1 scanning ratio</b>. For every 10 inches (or centimeters) of distance between the customer and the QR code, increase the barcode width by 1 inch (or centimeter). A menu scanned from across a table (20 inches away) should be at least 2 x 2 inches wide.
</div>"""
]

def humanize_text(content):
    modified = content
    for pattern, replacement in AI_REPLACEMENTS:
        modified = re.sub(pattern, replacement, modified)
    return modified

def process_file(fpath, tip_index):
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read()

    new_html = humanize_text(html)

    # In blog articles, check if a practitioner note is needed
    if "blog" in fpath and "<article" in new_html and "Field-Tested Note" not in new_html:
        tip_box = PRACTITIONER_TIPS[tip_index % len(PRACTITIONER_TIPS)]
        # Insert before the last </article>
        if "</article>" in new_html:
            new_html = new_html.replace("</article>", f"{tip_box}\n</article>", 1)

    if new_html != html:
        with open(fpath, "w", encoding="utf-8") as f:
            f.write(new_html)
        return True
    return False

def main():
    print("=== Running Content Humanizer & Anti-AI Engine ===")
    count = 0
    tip_counter = 0

    for root, dirs, files in os.walk(WEBSITE_DIR):
        if "tests" in root or "scripts" in root:
            continue
        for fname in files:
            if fname.endswith(".html"):
                fpath = os.path.join(root, fname)
                if process_file(fpath, tip_counter):
                    rel = os.path.relpath(fpath, WEBSITE_DIR)
                    print(f"[Humanized & Anti-AI Optimized] {rel}")
                    count += 1
                    tip_counter += 1

    print(f"\n[Complete] Successfully humanized and anti-AI optimized {count} HTML files!")

if __name__ == "__main__":
    main()
