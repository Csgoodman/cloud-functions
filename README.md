# Overview
This is a Google Cloud Functions (GCF) example, utilizing the [Open Weather Map API's Current Weather Data](https://openweathermap.org/current). You can deploy Google Cloud Functions from a variety of interfaces, but for this example we will use the Fivetran UI.

1. Place your working code in the source editor (main.py)
2. Specify what function in your script to call when GCF is triggered, and specify what Python function to call when the GCF is triggered.
3. Ensure that your requirements.txt file has any packages that are imported in your script.

# Open Weather Map API
To change what location you are targeting with the Open Weather Map API, download **city.list.json.gz** and locate your desired city ID [here](http://bulk.openweathermap.org/sample/).