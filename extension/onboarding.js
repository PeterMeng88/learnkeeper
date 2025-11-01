document.getElementById('startBtn').addEventListener('click', () => {
  chrome.storage.sync.set({isFirstTime: false}, () => {
    window.close();
  });
});

document.getElementById('tutorialBtn').addEventListener('click', () => {
  chrome.tabs.create({
    url: 'https://github.com/learnkeeper-io/learnkeeper#usage'
  });
});
