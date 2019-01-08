台7乙肇事統計地圖
================

data source: [警政署歷史交通事故資料](https://www.npa.gov.tw/NPAGip/wSite/lp?ctNode=12854&CtUnit=2633&BaseDSD=7&mp=3)

統計年份: 2014 ~ 2017



File Structure
==============

* `data.csv`: 所有 2014 ~ 2017 的台 7 乙事故資料 (A1, A2)
* `main.py`: 將所有事故資料轉換成 kml
* `t7b_mileage_sign.csv`: 台 7 乙所有里程樁
* `t7b_incident.kml`: 轉換後的 kml 檔


How To Use
==========

```
$ python main.py
$ ls
... t7b_incident.kml ...
```

將 t7b_incident.kml 上傳至 google mymaps 觀看


Web
===

Front-end

```
$ cd web
$ npm install
$ npm run dev   # local development
$ npm run build # build production dist
```

Backend

```
$ pipenv install
$ pipenv install gunicorn
$ pipenv run gunicorn -b 0.0.0.0:8888 app:app
```
