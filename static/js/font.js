import { library, dom, config } from "@fortawesome/fontawesome-svg-core";
import { faLocationDot, faSackDollar, faBars, faFire, faHeart, faBriefcase, faArrowUpRightFromSquare } from '@fortawesome/free-solid-svg-icons';
import { faThumbsUp } from '@fortawesome/free-regular-svg-icons';

config.mutateApproach = "sync";
library.add(faLocationDot, faSackDollar, faBars, faFire, faHeart, faBriefcase, faArrowUpRightFromSquare, faThumbsUp);

dom.watch();
