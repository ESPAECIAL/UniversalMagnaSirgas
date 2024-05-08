const ProjectedCRS = require('./ProjectedCRS');

describe('ProjectedCRS', () => {
    it('should not throw an error when instantiated directly', () => {
        let errorCaught;
        try {
            new ProjectedCRS();
            errorCaught = false;
        } catch (error) {
            errorCaught = true;
            expect(error.message).toBe("You can instantiate a not abstract class");
        }
        expect(errorCaught).toBe(false);
    });
});
