# Project Logs
Trace business requirements with system features and agreements in one view.

### Features in mind:

* ~~Export traceability to csv~~ **09-01**
* Generate MoM in Word or PDF
* Attach images and files in `Agreement` model
* Project Dashboard - low priority **starting**
* Generate Use Case Number - concatenation
* Finalize URL redirection
* Login!!! (Very basic thing lol)
* ~~Improve Data Entry/Import by CSV~~ **09-01**
* Batch Edit
* ~~Handling Sprints!~~ **09-09**
* Form for each feature: Use Case Format (Export to Word or PDF)
* Google Calendar Sync (Nice to Have)
* Auto update parent model (`Feature`) if all child models (`Ticket`) are done

---


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
2. Improved Filtering in admin
3. Added sample project data - BoC Trade. This is to avoid being too constricted with PEMC's use case.
4. Improvement: GrandParents as ForeignKey


### September 2, 2017 - Saturday

1. Data Prep - Project 2
2. Polished models
3. Added inlines for Project
4. Next: Focus on UX in traceability first,
5. Later: Management part. Sprints

### September 3, 2017 - Sunday

1. Issues: Filter in Django template view
--- Solved by adding logic in template view itself. Improve on this next time!
2. Please be guided by the flowcharts and ERD (See official GDrive)
3. Set up git in Atom!


### September 5, 2017 - Tuesday
1. Issue: not working bs3 collapse.js
2. Added base.html template
3. Started Simple and Functional Dashboard
4. Next:  
[ ] Finalize I/O of Requirements-Feature Mapping.  
[ ] Integrate `Ticket`, `Sprint` and `Agreement` models  


### September 9, 2017 - Saturday
1. `inclusion_tags` for feature status
2. Created `Sprint` model.
3. Polished other models.
4. Incorporated Sprint in project dashboard
5. import export `Ticket` model. Do note the templates for import and export are different.



### September 17, 2017 - Sunday
1. Project Dashboard enhancement (Counts, percentages, Dates, Workdays)
2. Added template tags - count business days
3. Auto update tickets based on **dates** for `Sprint` model


<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD

### September 28, 2017 - Sunday


=======
>>>>>>> parent of c259616... last minute notes on release and sprint
=======
>>>>>>> parent of c259616... last minute notes on release and sprint
=======
>>>>>>> parent of c259616... last minute notes on release and sprint
=======
>>>>>>> parent of c259616... last minute notes on release and sprint
### Next
1. UX/Styling
2. Auto update parent tickets based on child.
3. Polishing
4. Documentation on process flows.
5. Forms: update ticket statuses!
6. Login!!!


(What do I need to know?)

#### Project Dashboard

Use Case: I want to track the current status of the project delivery

* ~~Current Sprint~~  **Done 09-15**
* ~~Deadline~~  **Done 09-15**
* ~~Allocated Sprints for Project~~  **Done 09-15**
* ~~How many sprints per release~~ **Done 09-15**
* ~~Target release dates~~  **Done 09-15**
* ~~Sprint Statuses~~  **Done 09-15**

#### Release Page

Use Case: I want to check if all intended requirements for the release are met.

*   Release details (important dates, descriptions)
*  All requirements and corresponding features.
* Soon: Test Cases!

#### Requirements Page

Use Case: I want to check if all intended requirements for the whole project are met.

*  All requirements and corresponding features.
* Soon: Test Cases!


#### Sprint Page

Use Case: I want to be able to report what happened during the sprint.
must be able to:     
* view related features (and maybe related requirement)    
* update status on the spot  
* (nice to have) update logs
* generate report status/retrospective per sprint  
