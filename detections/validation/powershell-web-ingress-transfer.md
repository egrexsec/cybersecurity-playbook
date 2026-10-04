# PowerShell Web Ingress Transfer Validation

DET-2026-014 detects PowerShell script blocks that write retrieved web content to a file using either `WebClient.DownloadFile` or `Invoke-WebRequest -OutFile`. Exact and modified positives matched; three non-transfer controls stayed quiet. The authoritative Sigma source converts to official Splunk and Elastic outputs; the live Splunk lane uses raw XML until field normalization is complete.
