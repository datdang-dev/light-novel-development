# LND Studio Bootstrap

> **CRITICAL ARCHITECTURE FILE**
> All agents MUST read this file as their very first action to self-locate within the file system.

```yaml
# The absolute path to the root of the LND project workspace.
PROJECT_ROOT: "/home/datdang/working/lnd_dev"
```

## Agent Instruction
Whenever a workflow or YAML file references `{project-root}`, substitute it with the value of `PROJECT_ROOT` defined above.
