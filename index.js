const { chromium } = require('playwright');

module.exports = async (req, res) => {
    const browser = await chromium.launch();
    const page = await browser.newPage();
    await page.goto('https://www.baidu.com/');

    const title = await page.title();
    
    await browser.close();
    console.log(title);
    res.json({ title });
};
