package review;

import java.io.File;
import org.eclipse.equinox.app.IApplication;
import org.eclipse.equinox.app.IApplicationContext;
import org.knime.core.node.ExecutionMonitor;
import org.knime.core.node.workflow.WorkflowLoadHelper;
import org.knime.core.node.workflow.WorkflowManager;

/** Integration test entry point for KNIME 5.12; always run in an isolated workspace. */
public final class ReviewTest implements IApplication {
    public Object start(IApplicationContext context) throws Exception {
        File dir = new File(System.getenv("REVIEW_FIXTURE")).getCanonicalFile();
        var loaded = WorkflowManager.loadProject(dir, new ExecutionMonitor(), new WorkflowLoadHelper(dir));
        var workflow = loaded.getWorkflowManager();
        boolean ok = workflow.executeAllAndWaitUntilDone();
        System.out.println("REVIEW_NATIVE_RESULT " + ok);
        return ok ? EXIT_OK : Integer.valueOf(1);
    }
    public void stop() {}
}
