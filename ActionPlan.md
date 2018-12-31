## Action Plan for Complete Project (Revised) :

To complete the project we need to do the following task one by one.

- [x] Create frames of given video, first one every 5 seconds.

- [x] Detect faces from the frames. Should be able to detect multiple faces in one image.

- [ ] Detect hyper emotion from the faces. (In progress. Prototype can be expected in 2-3 days to a maximum of 4-5 days.)
    - [ ] Integrate Hyper Emotion Detection script into into code.

- [x] Use timestamps or array or something to store the exact time/frame for the trim.

- [x] For each hyper emotion(more like so much emotion), from the original video create a mini video containing 2 secs before the emotion and 2 secs after.

- [x] Include audio in those mini videos. Either don't remove it during the trim or add it appropriately as per the original later. 

- [x] Combine all the mini videos into a single.

- [ ] Perform Test Driven Development (TDD) using any testing framework.
    - [x] Perform TDD on the module.
    - [ ] Perform TDD on ML integrated code.

- [ ] Create documentation for the project.
    - [x] Use sphinx autodocs.
    - [ ] Write function docstrings in numpy format.
