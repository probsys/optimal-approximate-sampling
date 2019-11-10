// Macro for reading, sampling, and timing.
// ** @author: fsaad@mit.edu

#define READ_SAMPLE_TIME(key, \
        var_sampler, \
        struct_name, \
        func_read, \
        func_sample, \
        func_free, \
        var_path, \
        var_steps, \
        var_t, \
        var_x) \
    if(strcmp(var_sampler, key) == 0) { \
        struct struct_name s = func_read(var_path); \
        var_t = clock(); \
        for (int i = 0; i < var_steps; i++) { \
            var_x += func_sample(&s); \
        } \
        var_t = clock() - var_t; \
        func_free(s); \
    }
