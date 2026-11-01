// Background Service Worker for MyLogoQR Chrome Extension (Manifest V3)

chrome.runtime.onInstalled.addListener(() => {
  // Create Context Menus
  chrome.contextMenus.create({
    id: "mylogoqr_page",
    title: "Generate QR for this Page",
    contexts: ["page"]
  });

  chrome.contextMenus.create({
    id: "mylogoqr_selection",
    title: "Generate QR for '%s'",
    contexts: ["selection"]
  });

  chrome.contextMenus.create({
    id: "mylogoqr_link",
    title: "Generate QR for this Link",
    contexts: ["link"]
  });

  console.log("MyLogoQR Extension installed successfully.");
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  let content = "";
  if (info.menuItemId === "mylogoqr_selection") {
    content = info.selectionText || "";
  } else if (info.menuItemId === "mylogoqr_link") {
    content = info.linkUrl || "";
  } else if (info.menuItemId === "mylogoqr_page") {
    content = tab.url || "";
  }

  if (content) {
    chrome.storage.local.set({ contextQrData: content }, () => {
      // Open the action popup or set badge
      chrome.action.setBadgeText({ text: "QR" });
      chrome.action.setBadgeBackgroundColor({ color: "#2563EB" });
      setTimeout(() => {
        chrome.action.setBadgeText({ text: "" });
      }, 4000);
    });
  }
});
