# Project Logs
Trace business requirements with system features and agreements in one view.

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

Features in mind:
* Export traceability to csv
* Generate MoM in Word or PDF
* Attach images and files in `agreement` model
