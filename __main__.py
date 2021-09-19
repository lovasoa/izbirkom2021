
#!/usr/bin/env python3

# HOW TO USE:
# sudo apt-get install tesseract-ocr libtesseract-dev libleptonica-dev pkg-config tesseract-ocr-rus
# pip3 install pyppeteer tesserocr

import asyncio
from pyppeteer import launch
import tesserocr

img = "page.png"
url = 'http://www.primorsk.vybory.izbirkom.ru/region/izbirkom?action=show&root=252000008&tvd=4254005265098&vrn=100100067795849&prver=0&pronetvd=null&region=25&sub_region=25&type=242&report_mode=null'

async def main():
    browser = await launch({
        "headless": True,
        "defaultViewport": {
            "width":1920,
            "height":5800
      }})
    page = await browser.newPage()
    page.setDefaultNavigationTimeout(120000)
    await page.goto(url, {"waitUntil": "networkidle0"})
    await page.evaluate('''
        document.getElementById("election-results")
            .parentElement
            .setAttribute(
                "style", 
                "position: fixed; top: 0; left: 0; z-index: 999; width: 100%; background: white; height: 100%"
            )
    ''')
    await page.screenshot({'path': img, 'fullPage': 'true'})
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())

with tesserocr.PyTessBaseAPI(psm=tesserocr.PSM.AUTO_OSD, lang='rus') as api:
    api.SetImageFile(img)
    with open("results.txt", "w") as f:
        f.write(api.GetUTF8Text())
