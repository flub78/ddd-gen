# Design notes

Note to respect the separation of concern database metadata need to be at the business level. Previous implementation for exemple were used to define that a boolean was a checkbox in the database metadata. It was a mistake, from a business point of view it was a boolean. It is at the code generator level that the decision has to be made to use a checkbox or
something else to display it.

To avoid too many configuration parameters in the code generator is is possible to add classes (like in CSS) to help the code generators to make choices.
