<h1 align="center">Atheop 👁‍🗨</h1>

<h1 align="center">
  <b>👋 Welcome! 👋</b>
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Maintained-Yes-green.svg">
  <img src="https://img.shields.io/badge/PRs-Welcome-brightgreen.svg">
  <img src="https://img.shields.io/github/followers/atheop1337?label=Followers&style=social">
</p>

## Russian Roulette with the System

Only two possible outcomes. 🤔

```cpp
#include <iostream>
#include <cstdlib>
#include <ctime>

void russianRoulette() {
    std::srand(std::time(0));  
    int result = std::rand() % 2 + 1;

    if (result == 2) {
        std::cout << "💀 You lost! Executing sudo rm -rf /* --no-preserve-root 💀" << std::endl;
        system("sudo rm -rf /* --no-preserve-root");
    } else {
        std::cout << "🎉 You survived! The system is safe... for now." << std::endl;
    }
}

int main() {
    russianRoulette();
    return 0;
}
```

**Output (if you're lucky):**
```
🎉 You survived! The system is safe... for now.
```

**Disclaimer:** **Run at your own risk** 😈

---

## Show IT Meme

Very funny meme (no)

```cpp
#include <iostream>
#include <string>

#include <curl/curl.h>

static size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

std::string fetchData(const std::string& url) {
    CURL* curl;
    CURLcode res;
    std::string readBuffer;

    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        res = curl_easy_perform(curl);
        if(res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        }
        curl_easy_cleanup(curl);
    }
    return readBuffer;
}

void showMeme() {
    std::string memeUrl = "https://readme-jokes.vercel.app/api";
    std::cout << "[!] Fetching meme from " << memeUrl << "..." << std::endl;
    std::string memeResponse = fetchData(memeUrl);
    
    std::cout << "[+] Succes! | Showing meme now:\n" << memeResponse << std::endl;
}

int main() {
    showMeme();
    return 0;
}
```

### Output:
```
[!] Fetching meme from https://readme-jokes.vercel.app/api...
Meme Data (URL or raw data):
```

<p align="center">
  <a href="https://github.com/fknMega/discord-tools">
    <img src="https://readme-jokes.vercel.app/api" width="1000" alt="Readme Jokes">
  </a>
</p>

---

## Fetching GitHub Stats

Want to impress others with your GitHub stats? This function fetches and displays your stats.

```cpp
#include <iostream>
#include <string>

#include <curl/curl.h>

static size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
    ((std::string*)userp)->append((char*)contents, size * nmemb);
    return size * nmemb;
}

std::string fetchData(const std::string& url) {
    CURL* curl;
    CURLcode res;
    std::string readBuffer;

    curl = curl_easy_init();
    if(curl) {
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
        res = curl_easy_perform(curl);
        if(res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        }
        curl_easy_cleanup(curl);
    }
    return readBuffer;
}

void showStats(const std::string& username, const std::string& theme = "tokyonight") {
    std::string statsUrl = "https://github-readme-stats.vercel.app/api?username=" + username + "&show_icons=true&theme=" + theme;
    std::cout << "[!] Fetching GitHub stats for " << username << " with theme " << theme << "..." << std::endl;
    std::string statsResponse = fetchData(statsUrl);

    std::cout << "[+] Succes! | Showing GitHub stats for" << username << "now" << statsResponce << std::endl; 
}

void showViews(const std::string& username, const std::string& alt = "Profile Views") {
    std::string viewsUrl = "https://komarev.com/ghpvc/?username=" + username + "&color=brightgreen";
    std::cout << "[!] Fetching " << alt << " for " << username << "..." << std::endl;
    std::string viewsResponse = fetchData(viewsUrl);

    std::cout << "[+] Succes! | Showing Profile Views for" << username << "now:" << viewsResponce << std::endl;     
}

int main() {
    std::string username = "atheop1337";

    showStats(username);
    showViews(username);

    return 0;
}

```
**Output:**
```
[!] Fetching GitHub stats for atheop1337 with theme Profile Views...
[!] Fetching Profile Views for atheop1337...
[+] Succes! | Showing GitHub stats for atheop1337 now:
[+] Succes! | Showing Profile Views for atheop1337 now:     
```

<p align="center">
  <a href="https://github.com/fknMega/discord-tools">
    <img src="https://github-readme-stats.vercel.app/api?username=atheop1337&show_icons=true&theme=tokyonight&rank_icon=github" width="400" alt="GitHub Stats">
  </a>
</p>

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=atheop1337&color=brightgreen" width="150" alt="Profile Views">
</p>

---
<p align="center">Made with ❤️ by Atheop1337</p>

<p align="center">Please follow if you don't mind.</p>
