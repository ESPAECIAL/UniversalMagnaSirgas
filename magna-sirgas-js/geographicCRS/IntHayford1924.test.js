const IntHayford1924 = require('./IntHayford1924');

describe('IntHayford1924', () => {
    it('should not throw an error when instantiated directly', () => {
        let errorCaught;
        try {
            new IntHayford1924();
            errorCaught = false;
        } catch (error) {
            errorCaught = true;
            expect(error.message).toBe("You can instantiate a not abstract class");
        }
        expect(errorCaught).toBe(false);
    });
});