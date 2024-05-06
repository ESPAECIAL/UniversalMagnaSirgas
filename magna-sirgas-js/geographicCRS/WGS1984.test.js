const WGS1984 = require('./WGS1984');

describe('WGS1984', () => {
    it('should not throw an error when instantiated directly', () => {
        let errorCaught;
        try {
            new WGS1984();
            errorCaught = false;
        } catch (error) {
            errorCaught = true;
            expect(error.message).toBe("You can instantiate a not abstract class");
        }
        expect(errorCaught).toBe(false);
    });
});
