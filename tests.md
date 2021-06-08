# Manual testing on features

The first step of the testing process was to create the basic framework of this application and check if the attached links for navigation between sections work properly. Then the application was developed successively, section by section. During the development process, all the features were checked after they were included. Last proper manual testing included one more detailed checking if everything works as expected.

1. **Brand name link and Home link** - has been checked and confirmed that directs the user successfully to the Home page.
2. **All links settled in the top navigation bar** - have been checked that allow the user to navigate between individual pages like Home, Cocktail Collection, Register, Log In, Add Dream Recipe, Profile, Log Out.
3. **All links settled in the side navigation bar for mobile** - also have been checked that allow the user to navigate between individual pages.
4. **Image Carousel at the Home Page** - has been checked that scrolls right and left direction properly and gives a user visual experience together with the experience of interaction. Users can see the theme of the page during navigation
5. **Category dropdown selection at the Home Page** - has been checked that display properly cocktails category name and category description, and all elements are clickable and 
6. **Button nested at the Home Page** - has been checked and ensured that directs the user short way from content to add new recipe, but first to Register Page or Log In Page. 

7. **Social media icons settled in the footer** - has been checked and ensured that points the user to social media main pages and opens in a new tab.

# Validation 
When the site developed closer to the final stage, the next test was to check eventually errors in a code validation.
- **HTML** - passing code into The W3C Markup Validation Service brought some warnings, 

<img src="assets/docs/.jpg" style="margin: 0;">

- **CSS** - passing code into The W3C CSS Validation Service - Jigsaw brought no errors.
- **Java Script** - passing code to JSHint a static code analysis tool for JavaScript returned some metrics about missing "use strict" statement, despite this, the functionality of code worked for the application.

<img src="assets/docs/pictures/JS_Hint.jpg" style="margin: 0;">

- **PEP8** - check code for PEP8 requirements, passing code into PEP8 online returned one error 501 line too long

<img src="assets/docs/pictures/.jpg" style="margin: 0;">

# Other Tests
- **Google Chrome Developer Tools** - The further tests of the application were about to check responsiveness in all pages using devtools. Multiple tests on multiple desktop sizes confirmed that a structure works quite well on mobile devices as well as bigger desktop sizes. The tests were conducted mainly with the use of the Google Chrome browser. However, the research also covered other browsers such as Mozilla Firefox, Microsoft Edge, and Apple Safari. In general, after inspecting by use of the tools available in each browser, it was found that the application displays correctly and is responsive to different screen sizes. 

| Browser | Device | Compatibility |
| --- | --- | --- |
| Google Chrome | HP Spectre 13 | no problems occurred |
| Mozilla Firefox | HP Spectre 13 | no problems occurred |
| Microsoft Edge | HP Spectre 13 | no problems occurred |
| Apple Safari | iPad 5th gen | no problems occurred |


<img src="assets/docs/.jpg" style="margin: 0;">

- In addition, the test was performed live on devices such as Huawei P20, Samsung Galaxy S10, iPhone 11, iPad 9.7, HP Spectre 13, Asus Zenbook UX32A, iMac. The result was very good and shown that on all those screen devices website was responsive and displayed as expected.

- **Lighthouse web.dev** - Further tests were done by using Lighthouse open source, the performance result was good, no common issues were shown about timing, interactions, accesibility.

<img src="assets/docs/pictures/Lighthouse.jpg" style="margin: 0;">

- **Google Mobile-Friendly Test Tool** - Continuing subsequent tests included a test on mobile devices such as mobile phones, the entire application was checked with Google Mobile-Friendly Test Tool and showed that the design is friendly to such devices.

<img src="assets/docs/pictures/Mobile_friend.jpg" style="margin: 0;">

- **Grammarly** - Final tests were about to check grammar and spelling throughout the whole site and Readme file, page by page text was run through Grammarly application and showed several errors to correct.

