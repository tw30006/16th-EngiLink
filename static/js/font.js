import { library, dom, config } from "@fortawesome/fontawesome-svg-core";
import { faLocationDot, faSackDollar, faBars, faFire, faHeart, faBriefcase, faArrowUpRightFromSquare } from '@fortawesome/free-solid-svg-icons';
import { faThumbsUp } from '@fortawesome/free-regular-svg-icons';
import { faGoogle } from '@fortawesome/free-brands-svg-icons';
import { faGithub } from '@fortawesome/free-brands-svg-icons';

config.mutateApproach = "sync";
library.add(faLocationDot, faSackDollar, faBars, faFire, faHeart, faBriefcase, faArrowUpRightFromSquare, faThumbsUp,faGoogle, faGithub);

dom.watch();
