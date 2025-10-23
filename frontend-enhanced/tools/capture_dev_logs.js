import fs from "fs";
import path from "path";
import puppeteer from "puppeteer";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

async function runCapture() {
  const out = { console: [], requests: [], responses: [] };
  let browser;
  try {
    browser = await puppeteer.launch({
      args: ["--no-sandbox", "--disable-setuid-sandbox"],
    });
    const page = await browser.newPage();

    page.on("console", (msg) => {
      try {
        const text = msg.text();
        out.console.push({ type: msg.type(), text });
        console.log("[PAGE CONSOLE]", msg.type(), text);
      } catch (e) {
        console.error("console read error", e);
      }
    });

    page.on("request", (req) => {
      try {
        out.requests.push({
          url: req.url(),
          method: req.method(),
          headers: req.headers(),
          postData: req.postData(),
          resourceType: req.resourceType(),
          timestamp: Date.now(),
        });
        console.log("[REQUEST]", req.method(), req.url());
      } catch (e) {
        console.error("request read error", e);
      }
    });

    page.on("response", async (resp) => {
      try {
        const req = resp.request();
        let text;
        try {
          text = await resp.text();
        } catch (e) {
          text = "<non-text>";
        }
        out.responses.push({
          url: resp.url(),
          status: resp.status(),
          headers: resp.headers(),
          request: { method: req.method(), url: req.url() },
          body: text,
          timestamp: Date.now(),
        });
        console.log("[RESPONSE]", resp.status(), resp.url());
      } catch (e) {
        console.error("response read error", e);
      }
    });

    const target = process.argv[2] || "http://localhost:5173/";
    console.log("navigating to", target);
    await page
      .goto(target, { waitUntil: "networkidle2", timeout: 60000 })
      .catch((e) => console.error("goto error", e));

    const sleep = (ms) => new Promise((res) => setTimeout(res, ms));
    await sleep(1000);

    try {
      const [useDemoButton] = await page.$x(
        "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'use demo')]"
      );
      if (useDemoButton) {
        console.log("clicking Use demo");
        await useDemoButton.click();
        await sleep(500);
      } else {
        console.log("no Use demo button found");
      }
    } catch (e) {
      console.error("use demo click failed", e);
    }

    try {
      const submitHandle = await page.$(
        "form button[type=submit], button[type=submit]"
      );
      if (submitHandle) {
        console.log("submitting form");
        await submitHandle.click();
      } else {
        console.log("no submit button found");
      }
    } catch (e) {
      console.error("submit failed", e);
    }

    await sleep(3000);

    const outPath = path.resolve(__dirname, "dev_capture.json");
    try {
      fs.writeFileSync(outPath, JSON.stringify(out, null, 2));
      console.log("wrote capture to", outPath);
    } catch (e) {
      console.error("write file error", e);
    }

    await browser.close();
    process.exit(0);
  } catch (err) {
    console.error("capture script error", err);
    if (browser)
      try {
        await browser.close();
      } catch (e) {}
    process.exit(1);
  }
}

runCapture();
