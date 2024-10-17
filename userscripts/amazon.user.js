// ==UserScript==
// @name         Amazon Ukraine Customs Tax Calculator
// @namespace    https://www.amazon.com
// @version      1.0
// @description  Calculate Ukraine customs tax for Amazon products
// @author       Alexey ALERT Rubasheff
// @match        *://www.amazon.com/*
// @match        *://www.amazon.ae/*
// @match        *://www.amazon.be/*
// @match        *://www.amazon.ca/*
// @match        *://www.amazon.cn/*
// @match        *://www.amazon.co.jp/*
// @match        *://www.amazon.co.uk/*
// @match        *://www.amazon.co.za/*
// @match        *://www.amazon.com.au/*
// @match        *://www.amazon.com.br/*
// @match        *://www.amazon.com.mx/*
// @match        *://www.amazon.com.tr/*
// @match        *://www.amazon.com/*
// @match        *://www.amazon.de/*
// @match        *://www.amazon.eg/*
// @match        *://www.amazon.es/*
// @match        *://www.amazon.fr/*
// @match        *://www.amazon.in/*
// @match        *://www.amazon.it/*
// @match        *://www.amazon.nl/*
// @match        *://www.amazon.pl/*
// @match        *://www.amazon.sa/*
// @match        *://www.amazon.se/*
// @match        *://www.amazon.sg/*
// @exclude      *://*.amazon.*/ap/signin*
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function() {
    // 'use strict';

    // Функція для виконання запиту до API і обробки відповіді
    function getCustomsTax(price, currency) {
        console.info('Customs Tax Calculator: Getting customs tax for price:' + price + ' currency: ' + currency);
        var apiUrl = 'https://tax.alertua.pp.ua/calculate_api/?price=' + price + '&currency=' + currency;
        // Виконати запит до API
        GM_xmlhttpRequest({
            method: "GET",
            url: apiUrl,
            responseType: "json",
            onload: function(response) {
                if (response.status == 200) {
                    var data = response.response;
                    // Обробити отримані дані та відобразити результат поряд з ціною
                    var result = data.tax.toFixed(2) + ' ' + data.currency;
                    console.info('Customs Tax Calculator: Price:' + price + ' Currency: ' + currency + ' result: ' + result);
                    displayCustomsTax(result);
                } else {
                    console.error('Customs Tax Calculator: Failed to fetch customs tax data');
                }
            }
        });
    }

    // Функція для відображення розміру таможенних відрахувань поряд з ціною
    function displayCustomsTax(result) {
        // Знайти всі елементи з класом "a-price"
        var priceElements = document.getElementsByClassName('a-price');

        // Пройтися по кожному елементу та додати розмір таможенних відрахувань
        for (var i = 0; i < priceElements.length; i++) {
            var priceElement = priceElements[i];
            var customsTaxElement = document.createElement('span');
            customsTaxElement.textContent = ' + Tax: ' + result;
            priceElement.parentNode.insertBefore(customsTaxElement, priceElement.nextSibling);
        }
    }

    console.info('Customs Tax Calculator');
    // Отримати ціну та валюту з елементу сторінки та викликати функцію для обчислення таможенних відрахувань
    var priceElement = document.querySelector('.a-price span.a-offscreen');
    if (priceElement) {
        var price_raw = priceElement.textContent.trim();
        var regex = /[+-]?\d+(\.\d+)?/g;
        var price = price_raw.match(regex).map(function(v) { return parseFloat(v); });

        console.info('Customs Tax Calculator: Price found: ' + price);

        var currency = null;
        switch (document.location.hostname){
            case "www.amazon.com":
                currency = 'USD';
                break;
            case "www.amazon.de":
                currency = 'JPY';
                break;
            default:
                throw new Error(`${document.location.hostname} is NOT supported!`);
        }
        getCustomsTax(price, currency);
    } else {
        console.info('Customs Tax Calculator: No price element found');
    }
})();
