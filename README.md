#csc344-Project5

Write a Python program that collects, summarizes, and e-mails all the programming assignments for this course.

You should begin by organizing your assignments in a folder structure which will make this easier. I recommend something like:

    csc344
        a1
        a2
        a3
        a4
        a5

Assuming the programs are in subdirectories a1, a2, …, a5 of directory csc344, your program should:

-create a summary_ai.html (replacing i with the assignment number) file for each ai, which contains (in reasonably formatted, valid HTML):
        the name of each source file (linked to the file itself), along with the number of lines long the file is, and
        an alphabetized list of all identifiers used in the program (class, function, rule, variable etc. names), omitting duplicates. You do NOT need to specially filter keywords or builtin functions. Even though something like “for” in C isn’t really an identifier, we’ll be OK with including it. We won’t be OK with including punctuation which isn’t part of names, nor will we be ok with commented text. And don’t just delete all of your comments – you need to handle them!
-create a valid HTML web page in the csc344 directory called index.html with links to each of the summary files;
-create a tar.gz file containing all assignment sources, but excluding non-sources (executables, .class files, etc). Also included should be the html files created above. Be sure the links in the webpages work after extraction;
-prompt the user for an email address and send the tar.gz file.

