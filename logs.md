# Project Logs
Trace business requirements with system features and agreements in one view.

### Features in mind:

* ~~Export traceability to csv~~ **09-01**
* Generate MoM in Word or PDF
* Attach images and files in `agreement` model
* Project Dashboard - low priority
* Generate Use Case Number - concatenation
* Finalize URL redirection
* Login!!! (Very basic thing lol)
* ~~Improve Data Entry/Import by CSV~~ **09-01**
* Batch Edit


### August 26, 2017 - Saturday

* Set up git
* Set up Django
* Set up models relationships in Django Admin

| Model | Description|
| --- | --- |
| Project | Actual engagement. All other models are associated with one project|   
| Requirements |  Items in the Business Requirements Document (or any requirement documents from the client) |  
| Features  | Also known as Use Cases. Feature sounds more abstract. One feature can belong to many requirements. |  
| Tickets   |  Filed tickets per sprint/iteration in the project management tool. One `feature` can incur many tickets in many iteration |
| Agreement  |  Discussions egarding requirements and implementation. Can be external or internal. Can belong to a `requirement` or a `meeting` |

Next:
* Add `release` model - tentative
* Add `meeting` model
* Polish or model relationships in admin and models
* If done: start with the views and user experience in the app.



### August 28, 2017 - Monday

* Added release model
* Played with DetailView - Project, Requirement, Feature

Next:
* Add `release` model - tentative
* Add `meeting` model -- soon
* Polish or model relationships in admin and models
* If done: start with the views and user experience in the app.


Now onto user experience
1. Select project
2. View project dashboard
3. View Requirements by release

1. Input requirements based on BR
2. Tag by release - based on release planning.


### August 29, 2017 - Tuesday

1. Input SOW10 Data for more precise testing

### September 1, 2017 - Friday

1. Django-Import-Export library for importing and exporting data to csv
