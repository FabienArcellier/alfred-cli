Benefits
########

running in local and on CI platform
===================================

Alfred can be invoke on developper machine and on CI platform. It's a good practice to share the same behavior in local and on CI platform.
It's a good way to avoid the "it works on my machine" issue.

scaling with your team
======================

Alfred grows with your team. You can start with one command and then add more. When you feel that your command file is too crowded, you can restructure it into several files, or even separate it into several subfolders. Alfred is able to search all your orders by scanning a folder and its subfolders. It's all configurable.

loving mono-repository
======================

Alfred is built with the idea of being usable in a mono-repository which brings together several python, react, node projects in the same code repository. You can create several alfred sub-projects. At the root of the project, you will have access to all the commands of all the subprojects using the subproject name ``alfred project1 ci``.
