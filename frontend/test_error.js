const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('PAGE LOG:', msg.text()));
  page.on('pageerror', err => console.error('PAGE ERROR:', err));

  await page.goto('http://localhost:8000');
  
  // wait for input
  await page.waitForSelector('input[type="text"]');
  await page.type('input[type="text"]', '923609016');
  
  // hit enter
  await page.keyboard.press('Enter');
  
  // wait 5 seconds
  await new Promise(r => setTimeout(r, 5000));
  
  await browser.close();
})();
